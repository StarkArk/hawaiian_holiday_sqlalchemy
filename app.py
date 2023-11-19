# Import the dependencies.
# Dataframe toolkit
import numpy as np
import pandas as pd
import datetime as dt
# SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# Flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
# Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate App<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/<start><br/>"
        f"/api/v1.0/temp/<start>/<end>"
    )
# @app.route("/api/v1.0/precipitationa")
# def precipitation():
    
#     # Query dates and precipitation
#     session = Session(engine)
#     results = session.query(Measurement.date, Measurement.prcp).all()

#     # Create a dictionary using 'date' as the key and 'prcp' as the value
#     prcp_list = []

#     for date, prcp in results:
#         prcp_dict = {}
#         prcp_dict[date] = prcp
#         prcp_list.append(prcp_dict) 

#     session.close()

#     # Return the list of dates and precipitation
#     return jsonify(prcp_list)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # """Shows the precipitation data from 8-23-2016 
    #    to 8-23-2027 """
    # # return "hello"
    # # session = Session(engine)

    # # # Calculates dates for the last 12 months in the data
    # # recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # # recent_year = int(recent_date[0][0:4])
    # # recent_month = int(recent_date[0][5:7])
    # # recent_day = int(recent_date[0][8:10])
    # # last_date = dt.date(recent_year, recent_month, recent_day)
    year_back = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # # Query last 12 months of precipitation
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_back).all()

    # # Save Query as a dictionary
    # # prcp_ls_dict = [{"Date": prcp[0], "Precipitation": prcp[1]} for prcp in prcp_query]
    prcp_dict = {Date: prcp for Date, prcp in results}
    
    # prcp_ls_dict = {}

    session.close()

    return jsonify(prcp_dict)
    # return "hello"

    # prcp_list = []

    # for date, prcp in results:
    #     prcp_dict = {}
    #     prcp_dict[date] = prcp
    #     prcp_list.append(prcp_dict) 

    # session.close()

    # # Return the list of dates and precipitation
    # return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    # Find all the stations
    station_names = session.query(Station.name).distinct().all() 
    station_list = [station[0] for station in station_names]

    session.close()

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def temp_observations():
    
    session = Session(engine)

    # Convert 1 year prior to DateTime format
    year_back = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query the activity of each station for the previous 12 months
    station_row_count = session.query(Measurement.station, 
                                  func.count(Measurement.station)).\
                                  filter(Measurement.date >= year_back).\
                                  group_by(Measurement.station).\
                                  order_by(func.count(Measurement.station).desc()).\
                                  all()
    # Most active station
    top_station = station_row_count[0][0]
    # Query and list temps for the top_station
    top_station_temps = session.query(Measurement.date, Measurement.tobs).\
                                  filter(Measurement.station == top_station).\
                                  filter(Measurement.date >= year_back).\
                                  all()
    # List of dicts containing dates and temps for the previous 12 months
    temps_list = [{Date: temp} for Date, temp in top_station_temps]
    # Prepend station name(id)
    temps_list = [top_station] + temps_list

    session.close()

    return jsonify(temps_list)

@app.route("/api/v1.0/temp/<start>")
def start_date(start):
    
    session = Session(engine)

    # Find first and last date in data
    first_date = session.query(func.min(Measurement.date))[0][0]
    last_date = session.query(func.max(Measurement.date))[0][0]

    # Calculate min, max, avg temp for dataset based on a start date
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    if start >= first_date and start <= last_date:
        agg_temps = session.query(*sel).filter(Measurement.date >= start).all()[0]
        tmin, tmax, tavg = agg_temps[0], agg_temps[1], agg_temps[2],

        return (
            f"Min Temp: {tmin}</br>"
            f"Max Temp: {tmax}</br>"
            f"Avg Temp: {round(tavg, 1)}"
        )
    else:
        return f"Date entered is not in the data, please use a date between {first_date} and {last_date}"

    session.close()

@app.route("/api/v1.0/temp/<start>/<end>")
def date_range(start, end):
    
    session = Session(engine)

    # Find first and last date in data
    first_date = session.query(func.min(Measurement.date))[0][0]
    last_date = session.query(func.max(Measurement.date))[0][0]

    # Calculate min, max, avg temp for dataset based on a start and end date
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    if start >= first_date and start <= last_date and end >= start and end <= last_date:
        agg_temps = session.query(*sel).filter(Measurement.date >= start).\
                                        filter(Measurement.date <= end)[0]
        tmin, tmax, tavg = agg_temps[0], agg_temps[1], agg_temps[2],

        return (
            f"Min Temp: {tmin}</br>"
            f"Max Temp: {tmax}</br>"
            f"Avg Temp: {round(tavg, 1)}"
        )
    else:
        return f"Start and end date range entered is not in the data, please use dates between {first_date} and {last_date}"

    session.close()

if __name__ == "__main__":
    app.run(debug=True)
