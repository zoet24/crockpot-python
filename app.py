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
        recIngIds.pop(0)
        for recIngId in recIngIds:
            recDB_ingName = ObjectId(recIngId)
            recDB_ingNames.append(recDB_ingName)

        # Format recipe ingredient quantities to get quantities for 1 portion
        recServes = request.form.get("serves")
        recDB_ingNums = request.form.getlist("ingredientNum")
        recDB_ingNums.pop(0)
        recDB_ingNumsOne = []
        for recDB_ingNum in recDB_ingNums:
            print(recDB_ingNum)
            print(recServes)
            recDB_ingNumOne = float(recDB_ingNum)/float(recServes)
            print(recDB_ingNumOne)
            recDB_ingNumsOne.append(recDB_ingNumOne)

        # Format recipe ingredient names
        recDB_recCats = []
        recCatIds = request.form.getlist("recipeCategories")
        recCatIds.pop(0)

        for recCatId in recCatIds:
            recDB_recCat = ObjectId(recCatId)
            recDB_recCats.append(recDB_recCat)

        # Remove hidden add/remove value from form entries
        recDB_ingUnits = request.form.getlist("ingredientUnit")
        recDB_ingUnits.pop(0)

        recDB_instructions = request.form.getlist("instructions")
        recDB_instructions.pop(0)

        recDB_notes = request.form.getlist("notes")
        recDB_notes.pop(0)

        # Define new recipe for Mongo db
        recDB = {
            "name": request.form.get("name").title(),
            "url": recUrl,
            "time": request.form.get("time"),
            "image": request.form.get("image"),
            "ingredientName": recDB_ingNames,
            "ingredientNum": recDB_ingNumsOne,
            "ingredientUnit": recDB_ingUnits,
            "instructions": recDB_instructions,
            "notes": recDB_notes,
            "recipeCategories": recDB_recCats,
            "user": ObjectId("624712f53b6773d36014fcb5"),
        }

        mongo.db.recipes.insert_one(recDB)

        # Find new ID and redirect to new recipe
        newRecDB_Id = list(mongo.db.recipes.find().skip(mongo.db.recipes.count() - 1))[0]["_id"]

        return redirect(url_for("viewRecipe", rec_id=newRecDB_Id))

    # Get all recipe categories, all ingredients and a single recipe from Mongo
    recCatsDB = list(mongo.db.recipeCategories.find())
    ingsDB = list(mongo.db.ingredients.find())

    return render_template("pages/add_recipe/add_recipe.html",
                            recCats=recCatsDB,
                            ings=ingsDB)


@app.route("/browse")
def browse():
    # Get all recipes from Mongo db
    recsDB = list(mongo.db.recipes.find())

    return render_template("pages/browse_recipe/browse_recipe.html",
                            recs=recsDB)


@app.route("/deleteRecipe/<rec_id>")
def deleteRecipe(rec_id):
    rec = mongo.db.recipes.find_one({"_id": ObjectId(rec_id)})
    mongo.db.recipes.remove({"_id": ObjectId(rec_id)})

    return redirect(url_for("browse"))


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