# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///NHTSA.db")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
ratings = Base.classes.Ratings

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/overallrating<br/>"
        f"/api/v1.0/ratings"
    )


@app.route("/api/v1.0/overallrating")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all averall ratings"""
    # Query all passengers
    results = session.query(ratings.overall_rating).all()

    session.close()

    # Convert list of tuples into normal list
    all_overall_rating = list(np.ravel(results))

    return jsonify(all_overall_rating)


@app.route("/api/v1.0/ratings")
def Ratings():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Ratings"""
    # Query all Ratings
    results = session.query(ratings.year_make_model, ratings.overall_rating, ratings.frontal_crash, ratings.side_crash, ratings.rollover, ratings.safety_concerns).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_ratings
    all_ratings = []
    for year_make_model, overall_rating,frontal_crash, side_crash, rollover, safety_concerns in results:
        Ratings_dict = {}
        Ratings_dict["year_make_model"] = year_make_model
        Ratings_dict["overall_rating"] = overall_rating
        Ratings_dict["frontal_crash"] = frontal_crash
        Ratings_dict["side_crash"] = side_crash
        Ratings_dict["rollover"] = rollover
        Ratings_dict["safety_concerns"] = safety_concerns
        all_ratings.append(Ratings_dict)

    return jsonify(all_ratings)


if __name__ == '__main__':
    app.run(debug=True)