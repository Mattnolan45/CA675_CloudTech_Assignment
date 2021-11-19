from google.cloud import bigquery
from google.cloud.bigquery import client
from google.oauth2 import service_account



def creatBigQueryClient():
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
    SERVICE_ACCOUNT_FILE = 'cloudtechassignment2-37735bc6e7e7.json'

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return bigquery.Client(credentials=credentials)


class RankedAirline():
   
   def __init__(self, name,totalDelay):
        self.name = name
        self.totalDelay = totalDelay


class FlightResult():

    def __init__(self,carrierName,origin,dest,dep_delay,air_time,distance):
        self.carrierName = carrierName
        self.origin = origin
        self.dest = dest
        self.dep_delay = dep_delay
        self.air_time = air_time
        self.distance = distance


class LocationResult():

    def __init__(self,name,code) :
        self.name = name
        self.code = code
        
