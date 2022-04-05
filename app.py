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


@app.route("/<recipe_id>")
def view_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    ingredients = mongo.db.ingredients

    # Get array of ingredient names from Mongo ingredients db
    ingNames = []
    for ing in recipe["ingredientName"]:
        ingName = ingredients.find_one({"_id": ObjectId(ing)})["name"]
        ingNames.append(ingName)

    # Zip ingredient names, quantities and units into matrix
    ings = zip(ingNames,
               recipe["ingredientNum"],
               recipe["ingredientUnit"])

    return render_template("pages/view_recipe/view_recipe.html",
                           recipe=recipe,
                           ings=ings)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) # Change to false on deploy