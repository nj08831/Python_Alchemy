
#imports
from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


# Create an app, being sure to pass __name__
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Define what to do when a user hits the precipitation route
@app.route("/precipitation")
def precip():

    # Query of Date and Precipitation values
    precip_last = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').all()

    # Convert list of tuples into normal list
    all_values = list(np.ravel(precip_last))

    return jsonify(precip_last)

# Define what to do when a user hits the station route
@app.route("/stations")
def stations():
    
    station_freq = session.query( Measurement.station ,func.count(Measurement.station)).group_by(Measurement.station).order_by(desc(func.count(Measurement.station))).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station_freq))
    
    return jsonify(station_freq)

@app.route("/tobs")
def temps():
    
    lytemps = session.query(Measurement.date, Measurement.tobs, Measurement.station).filter(Measurement.date == '2016-08-22').all()

    # Convert list of tuples into normal list
    ly_temp = list(np.ravel(lytemps))
    
    return jsonify(ly_temp)



if __name__ == "__main__":
    app.run(debug=True)
