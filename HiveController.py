import re

import json
from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
from google.oauth2 import service_account
import google.auth


#with open(r'C:\Users\MatthewNolan.MATNOLLAPTOP\Downloads\cloudtechassignment2-e713ab3ab806.json') as source:
#   info = json.load(source)

#print(info)

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
SERVICE_ACCOUNT_FILE = r'C:\Users\MatthewNolan.MATNOLLAPTOP\Downloads\cloudtechassignment2-37735bc6e7e7.json'

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

#credentials, project_id = google.auth.default()

def submit_job(project_id, region, cluster_name):
    # Create the job client.

    job_client = dataproc.JobControllerClient(
        credentials=credentials,
        client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format(region)}
    )

    job = {
        "placement": {"cluster_name": cluster_name},
        "hive_job": { 
            "query_list" : {
                "queries" : [ "SELECT * FROM flightdata_db LIMIT 5;"]
            }
        }
    }

    operation = job_client.submit_job_as_operation(
        request={"project_id": project_id, "region": region, "job": job}
    )
    response = operation.result()

    matches = re.match("gs://(.*?)/(.*)", response.driver_output_resource_uri)

    output = (
        storage.Client()
        .get_bucket(matches.group(1))
        .blob(f"{matches.group(2)}.000000000")
        .download_as_string()
    )

    print(f"Job finished successfully: {response}")

projectId = "cloudtechassignment2"
region = "europe-west1"
clusterName = "cluster-d270"

submit_job(projectId,region,clusterName)

