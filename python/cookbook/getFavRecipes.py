import os
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


def getFavRecipes():
    recsDB = list(mongo.db.recipes.find())
    user = mongo.db.users.find_one({"username": session["user"]})
    userFavRecs = user["isFav"]

    # Get favourite recipes
    userFavRecsIds = []
    userFavRecsNames = []
    userFavRecsImages = []

    for rec in userFavRecs:
        userFavRec_id = rec
        userFavRec_name = mongo.db.recipes.find_one({"_id": ObjectId(rec)})["name"]
        userFavRec_image = mongo.db.recipes.find_one({"_id": ObjectId(rec)})["image"]

        userFavRecsIds.append(userFavRec_id)
        userFavRecsNames.append(userFavRec_name)
        userFavRecsImages.append(userFavRec_image)

    userFavRecs = zip(userFavRecsIds,
                      userFavRecsNames,
                      userFavRecsImages)

    return userFavRecs