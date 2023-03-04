# import dependencies
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine,reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station



#initialize app
app = Flask(__name__)

#create routes

#Homepage
@app.route("/")
def home():
    return (

    f"Honolulu,Hawaii Climate Analysis. <br/>"
    f"Paths available<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/start/end<br/><br/><br/>"
    f"*Hint: For start and end date paths, please input as YYYY-mm-dd<br/>"
)
#Precipitation Analysis
@app.route("/api/v1.0/precipitation")
def precip_analysis():
#    Create session
    session = Session(bind=engine)

#    Find the most recent date in the data set.
    recent_date_result=session.query(measurement.date).order_by(measurement.date.desc()).first()
    for result in recent_date_result:
        recent_date = result
    recent_date = dt.datetime.strptime(recent_date,"%Y-%m-%d")
# Calculate one year ago and query data
    year_ago = recent_date - dt.timedelta(days=365)
    last_year_data = session.query(measurement.date,measurement.prcp).filter(measurement.date > year_ago).all()
    session.close()
# Convert results to list of dictionaries and return results
    results = []
    for date,prcp in last_year_data:
        precip_dict = {}
        precip_dict["precipitation"] = prcp
        precip_dict["date"] = date
        results.append(precip_dict)
    return jsonify(results)

#JSON Station List
@app.route("/api/v1.0/stations")
def stations():
# Create session
    session = Session(bind=engine) 
# Create Query and close session
    station_list = session.query(station.station,station.name).all()
    session.close()
# Convert results to dictionary and return results
    results = []
    for id,name in station_list:
        station_dict = {}
        station_dict["Station ID"] = id
        station_dict["Station Name"] = name
        results.append(station_dict)
    return jsonify(results)

#Date and Temps for Active Station
@app.route("/api/v1.0/tobs")
def tobs():
# Create session
    session = Session(bind=engine) 
# Create Query
    station_freq = session.query(measurement.station,func.count(measurement.station)).\
           group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    active_station = station_freq[0][0]
#    Find the most recent date in the data set.
    recent_date_result=session.query(measurement.date).order_by(measurement.date.desc()).first()
    for result in recent_date_result:
        recent_date = result
    recent_date = dt.datetime.strptime(recent_date,"%Y-%m-%d")
# Calculate one year ago and query data
    year_ago = recent_date - dt.timedelta(days=365)
    year_temps = session.query(measurement.date,measurement.tobs).\
                  filter(measurement.date > year_ago).\
                  filter(measurement.station == active_station).\
                  group_by(measurement.date).all()
    session.close()
# Convert results to dictionary and return results
    results = []
    for date,temp in year_temps:
        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict["Temperature"] = temp
        results.append(temp_dict)
    return jsonify(results)

#Temp for Time Range
@app.route("/api/v1.0/<start>")
def variable_start(start):
    # Create session
    session = Session(bind=engine) 
    start_date_results = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),\
                                       func.max(measurement.tobs).\
                                        filter(measurement.date >= start)).all()
    session.close()
    # Compile results and return
    results = []
    for min,avg,max in start_date_results:
        start_dict = {}
        start_dict["Minimum Temperature"] = min
        start_dict["Average Temperature"] = avg
        start_dict["Maximum Temperature"] = max
        results.append(start_dict)
    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def variable_start_end(start,end):
    # Create session
    session = Session(bind=engine) 
    start_date_results = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),\
                                       func.max(measurement.tobs).\
                                        filter(measurement.date >= start).\
                                        filter(measurement.date <= end)).all()
    session.close()
   # Compile results and return
    results = []
    for min,avg,max in start_date_results:
        start_end_dict = {}
        start_end_dict["Minimum Temperature"] = min
        start_end_dict["Average Temperature"] = avg
        start_end_dict["Maximum Temperature"] = max
        results.append(start_end_dict)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)