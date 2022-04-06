"""
NAMING CONVENTION:
- Item from database should be suffixed by DB (eg. ingsDB)
- Item to be passed to app should not (eg. ings)
- If you are referencing a property of an item the syntax is item_property (eg. name of a recipe is rec_name)
- Shortcuts:
    - Ingredient => ing
    - Recipe => rec
    - Category => cat
"""

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


@app.route("/1")
def index():
    return render_template("pages/index/index.html")


# 624713793b6773d36014fcb8 --> Spag bol
@app.route("/viewRecipe/<rec_id>")
def view_recipe(rec_id):
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

    return render_template("pages/view_recipe/view_recipe.html",
                           rec=recDB,
                           ings=ings,
                           recCats=recCat_names)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) # Change to false on deploy