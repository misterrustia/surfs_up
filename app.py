# import dependencys
import numpy as np
import datetime as dt 
import pandas as pd 


# import SQLAlchemy dependencies 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, 

# import flask depends
from flask import Flask, jsonify 

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

#create variable for each class so that we can reference them later 
Measurement = Base.classes.measurement
Station = Base.classes.station


# create a session link from python to our database with the following code 
session = Session(engine)

# create flask application called "app"
app=Flask(__name__)
# all routes go after this 

# name will be set to what ever is running the code, if we put this in something else the name will change to 
#to what ever is running this, if we run directly with python app.py the name will be "main"

#define welcome route 
@app.route("/")

# create fnc 
def welcome():
    return(
        '''
        Welcome to the Climate Analysis API!
        Available Routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
        /api/v1.0/tobs
        /api/v1.0/temp/start/end
        ''')
        
@app.route("/api/v1.0/precipitation")

def precipitation():
    prev_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date:prcp for date, prcp in precipitation}
    return jsonify(precip)



@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations = stations)


# prev year is object with a year of days from 8,23 and is the filter for the measurement 
# measurement data being queried from session in SQLA 


# Jsonify in a fnc to convert dictionarys to JSON files 

@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station =='USC00519281').\
    filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
        
    return jsonify(temps=temps)


#cal date 1 yr from last date in DB
#query primary stayion for all temp obs from prvs year
#numpy ravel into 1 d array then convert into list
#temps = a list of the 1 d aray numpy usese ravel to create from the results 


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")


def stats(start=None, end=None):
    sel=[func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)


    results = session.query(*sel).\
            filter(Measurement.date >=start).\
                filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)



# sel is a list of querys using fnc on total observations data in SQLA
# pay attention to the asterix as allows results to have multiple objects come from sel and into results


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port = 5000)

