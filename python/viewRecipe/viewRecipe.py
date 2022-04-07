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


def viewRecipeData(rec_id):
    # Get all recipe categories, all ingredients and a single recipe from Mongo
    recCatsDB = mongo.db.recipeCategories
    ingsDB = mongo.db.ingredients
    recDB = mongo.db.recipes.find_one({"_id": ObjectId(rec_id)})

    # Get array of recipe category names from Mongo recipe categories db
    recCat_names = []
    for recCat in recDB["recipeCategories"]:
        recCat_name = recCatsDB.find_one({"_id": ObjectId(recCat)})["name"]
        recCat_names.append(recCat_name)

     # Get array of ingredient names from Mongo ingredients db
    ing_names = []
    for ing in recDB["ingredientName"]:
        ing_name = ingsDB.find_one({"_id": ObjectId(ing)})["name"]
        ing_names.append(ing_name)

    # Zip ingredient names, quantities and units into matrix
    ings = zip(ing_names,
               recDB["ingredientNum"],
               recDB["ingredientUnit"])

    # Get the user who created the recipe from Mongo users db
    recDB_user = recDB["user"]
    user = mongo.db.users.find_one({"_id": ObjectId(recDB_user)})
    
    return recDB, ings, recCat_names, user