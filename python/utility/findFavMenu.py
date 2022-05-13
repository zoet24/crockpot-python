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


def findFavMenu():
    # Find user and all fav/menu recipes
    user = mongo.db.users.find_one({"_id": ObjectId("624715013b6773d36014fcbc")})
    isFav = user["isFav"]

    isMenu = []
    for rec in user["isMenu"]:
        isMenu.append(rec["id"])

    return isFav, isMenu