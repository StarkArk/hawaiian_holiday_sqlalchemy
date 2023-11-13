# Import the dependencies.
from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

# Dataframe toolkit
import numpy as np
import pandas as pd
import datetime as dt

# SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, text, exc

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False, pool_pre_ping=True).connect()


# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)
# reflect the tables
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
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
    return(
        f"Welcome to the Hawaii Climate App<br/>"
        f"Available Routes:<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Shows the precipitation data from 8-23-2016 
       to 8-23-2027 """
    
    # Calculates dates for the last 12 months in the data
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_year = int(recent_date[0][0:4])
    recent_month = int(recent_date[0][5:7])
    recent_day = int(recent_date[0][8:10])
    last_date = dt.date(recent_year, recent_month, recent_day)
    year_back = last_date - dt.timedelta(days=365)

    # Query last 12 months of precipitation
    prcp_query = session.query(Measurement.date, 
                           Measurement.prcp).filter(Measurement.date >= year_back).\
                                             order_by(Measurement.date).\
                                             all()
    
    # Save Query as a dictionary
    prcp_ls_dict = [{"Date": prcp[0], "Precipitation": prcp[1]} for prcp in prcp_query]
    
    return jsonify(prcp_ls_dict)

if __name__ == "__main__":
    app.run(debug=True)
