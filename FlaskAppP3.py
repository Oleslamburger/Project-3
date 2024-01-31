# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
import datetime as dt

app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Data/NHTSA.db.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
# Measurement = Base.classes.measurement
# Station = Base.classes.station

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    return(f"Aloha! If using start or start/end routes please format in YYYY-D-M format.<br/>"
            f"/api/v1.0/precipitation<br/>"
           f"/api/v1.0/stations<br/>"
           f"/api/v1.0/tobs<br/>"
           f"/api/v1.0/start<br/>"
           f"/api/v1.0/start/end")