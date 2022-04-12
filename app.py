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
from python.addRecipe.addRecipe import addRecipePost
from python.viewRecipe.viewRecipe import viewRecipeData


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("pages/index/index.html")


@app.route("/addRecipe", methods=["GET", "POST"])
def addRecipe():
    if request.method == "POST":
        # python > addRecipe > addRecipe.py
        addRecipePost()

        # Find new ID and redirect to new recipe
        newRecDB_Id = list(mongo.db.recipes.find().skip(mongo.db.recipes.count() - 1))[0]["_id"]

        return redirect(url_for("viewRecipe", rec_id=newRecDB_Id))

    # Get all recipe categories, all ingredients categories and all ingredients from Mongo
    ingCatsDB = list(mongo.db.ingredientCategories.find())
    recCatsDB = list(mongo.db.recipeCategories.find())
    ingsDB = list(mongo.db.ingredients.find())

    return render_template("pages/add_recipe/add_recipe.html",
                            ingCats=ingCatsDB,
                            recCats=recCatsDB,
                            ings=ingsDB)


@app.route("/addIng", methods=["POST"])
def addIng():
    # Format recipe url
    ingUrl = request.form.get("name").lower().replace(' ', '-')

    ingDB = {
        "name": request.form.get("name").title(),
        "url": ingUrl,
        "category": ObjectId(request.form.get("category"))
    }

    mongo.db.ingredients.insert_one(ingDB)

    return redirect(url_for("addRecipe"))


@app.route("/addCat", methods=["POST"])
def addCat():
    # Format recipe url
    catUrl = request.form.get("name").lower().replace(' ', '-')

    catDB = {
        "name": request.form.get("name").title(),
        "url": catUrl
    }

    mongo.db.recipeCategories.insert_one(catDB)

    return redirect(url_for("addRecipe"))


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


@app.route("/editRecipe/<rec_id>", methods=["GET", "POST"])
def editRecipe(rec_id):
    # python > viewRecipe > viewRecipe.py
    data = viewRecipeData(rec_id)
    recDB = data[0]
    ings = data[1]

    # Get all recipe categories, all ingredients categories and all ingredients from Mongo
    ingCatsDB = list(mongo.db.ingredientCategories.find())
    recCatsDB = list(mongo.db.recipeCategories.find())
    ingsDB = list(mongo.db.ingredients.find())

    # Need to zip ingredients
    # Need to get recipeNames not IDs
    # Maybe write similar (not same) viewRecipe?

    return render_template("pages/edit_recipe/edit_recipe.html",
                            ingCats=ingCatsDB,
                            recCats=recCatsDB,
                            ingsAll=ingsDB,
                            rec=recDB,
                            ingsRec=ings)


# 624713793b6773d36014fcb8 --> Spag bol
@app.route("/viewRecipe/<rec_id>")
def viewRecipe(rec_id):
    # python > viewRecipe > viewRecipe.py
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