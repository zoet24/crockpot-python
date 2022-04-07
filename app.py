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
from python.viewRecipe.viewRecipe import viewRecipeData


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/1")
def index():
    return render_template("pages/index/index.html")


@app.route("/addRecipe", methods=["GET", "POST"])
def addRecipe():
    if request.method == "POST":
        # Format recipe url
        recUrl = request.form.get("name").lower().replace(' ', '-')

        # Format recipe ingredient names
        recDB_ingNames = []
        recIngIds = request.form.getlist("ingredientName")
        for recIngId in recIngIds:
            recDB_ingName = ObjectId(recIngId)
            recDB_ingNames.append(recDB_ingName)

        # Format recipe ingredient quantities
        recServes = request.form.get("serves")

        # Format recipe ingredient names
        recDB_recCats = []
        recCatIds = request.form.getlist("recipeCategories")
        for recCatId in recCatIds:
            recDB_recCat = ObjectId(recCatId)
            recDB_recCats.append(recDB_recCat)

        # Define new recipe for Mongo db
        recDB = {
            "name": request.form.get("name").title(),
            "url": recUrl,
            "time": request.form.get("time"),
            "image": request.form.get("image"),
            "ingredientName": recDB_ingNames,
            "ingredientNum": request.form.getlist("ingredientNum"),
            "ingredientUnit": request.form.getlist("ingredientUnit"),
            "instructions": request.form.getlist("instructions"),
            "notes": request.form.getlist("notes"),
            "recipeCategories": recDB_recCats,
            "user": ObjectId("624712f53b6773d36014fcb5"),
        }

        mongo.db.recipes.insert_one(recDB)
        # print(recDB)

        return redirect(url_for("index"))

    # Get all recipe categories, all ingredients and a single recipe from Mongo
    recCatsDB = list(mongo.db.recipeCategories.find())
    ingsDB = list(mongo.db.ingredients.find())

    return render_template("pages/add_recipe/add_recipe.html",
                            recCats=recCatsDB,
                            ings=ingsDB)


# 624713793b6773d36014fcb8 --> Spag bol
@app.route("/viewRecipe/<rec_id>")
def viewRecipe(rec_id):
    data = viewRecipeData(rec_id)
    recDB = data[0]
    ings = data[1]
    recCat_names = data[2]
    user = data[3]

    return render_template("pages/view_recipe/view_recipe.html",
                           rec=recDB,
                           ings=ings,
                           recCats=recCat_names,
                           user=user)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) # Change to false on deploy