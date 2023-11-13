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

from sqlalchemy import create_engine, exc

# e = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False, pool_pre_ping=True)
e = create_engine("sqlite:///Resources/hawaii.sqlite", pool_recycle=3600, echo=True)
c = e.connect()

try:
    # suppose the database has been restarted.
    c.execute(text("SELECT * FROM measurement"))
    c.close()
except exc.DBAPIError as e:
    # an exception is raised, Connection is invalidated.
    if e.connection_invalidated:
        print("Connection was invalidated!")

# after the invalidate event, a new connection
# starts with a new Pool
c = e.connect()
c.execute(text("SELECT * FROM measurement"))


# engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False, pool_pre_ping=True).connect()


# # reflect an existing database into a new model
# Base = automap_base()
# Base.prepare(autoload_with=engine)
# # reflect the tables
# Base.classes.keys()

# # Save references to each table
# Measurement = Base.classes.measurement
# Station = Base.classes.station

# # Create our session (link) from Python to the DB
# session = Session(engine)