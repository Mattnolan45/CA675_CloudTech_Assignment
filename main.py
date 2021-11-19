
from flask import Flask, render_template,request
import bqController

app = Flask(__name__)


client = bqController.creatBigQueryClient()

# get most reliable airlines based on total delay
TopAirlines = client.query(""" 
            SELECT carrier_name, Sum(dep_delay) as totalDelay 
            FROM `cloudtechassignment2.cloudtech.flightdata_db` 
            group by carrier_name 
            order by totalDelay asc 
            limit 5""")

Toplist = [ bqController.RankedAirline(t[0],t[1]) for t in TopAirlines] 

# get least reliable airlines based on total delay           
worstAirlines = client.query("""
            SELECT carrier_name, Sum(dep_delay) as totalDelay 
            FROM `cloudtechassignment2.cloudtech.flightdata_db` 
            group by carrier_name 
            order by totalDelay desc  
            limit 5
            """)

worstlist = [ bqController.RankedAirline(w[0],w[1]) for w in worstAirlines] 


# get list of origins
originQuery = client.query("""
            SELECT distinct codesdb.city_name,flightdb.origin
            FROM cloudtechassignment2.cloudtech.flightdata_db as flightdb 
            JOIN cloudtechassignment2.cloudtech.citycodes_db as codesdb ON flightdb.origin = codesdb.city_code
            order by codesdb.city_name asc 
            """)

# generate list of origins
originList = [bqController.LocationResult(o[0],o[1]) for o in originQuery] 


# get list of destinations
destQuery = client.query("""
            SELECT distinct codesdb.city_name,flightdb.dest
            FROM cloudtechassignment2.cloudtech.flightdata_db as flightdb 
            JOIN cloudtechassignment2.cloudtech.citycodes_db as codesdb ON flightdb.dest = codesdb.city_code
            order by codesdb.city_name asc 
            """)

# get list of destinations
destList = [ bqController.LocationResult(d[0],d[1]) for d in destQuery]

@app.route('/')
def root():
    return render_template('index.html',originList=originList, destList=destList, TopAirlines=Toplist, worstAirlines=worstlist)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/search",methods=["POST"])
def getRoutes():
    origin = request.form.get("origin")
    dest = request.form.get("dest")

    flightQuery = "SELECT carrier_name,dep_delay,air_time,distance FROM cloudtech.flightdata_db WHERE origin = '{}' AND dest = '{}'".format(origin,dest)
    flightQuery_job = client.query(flightQuery)

    originNameQuery = "SELECT city_name FROM cloudtechassignment2.cloudtech.citycodes_db WHERE city_code = '{}' ".format(origin)
    originQuery_job = client.query(originNameQuery)
    originName = [o[0] for o in originQuery_job]

    destNameQuery = "SELECT city_name FROM cloudtechassignment2.cloudtech.citycodes_db WHERE city_code = '{}' ".format(dest)
    destQuery_job = client.query(destNameQuery)
    destName = [d[0] for d in destQuery_job]

    resultList = [ bqController.FlightResult(r[0],originName[0], destName[0], r[1], r[2], r[3]) for r in flightQuery_job]

    return render_template('searchResult.html',resultList=resultList)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
