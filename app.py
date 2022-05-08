"""
NAMING CONVENTION:
- Item from database should be suffixed by DB (eg. ingsDB)
- Item to be passed to app should not (eg. ings)
- If you are referencing a property of an item the syntax is item_property (eg. name of a recipe from the app is rec_name)
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
from python.cookbook.getFavRecipes import getFavRecipes
from python.cookbook.getMyRecipes import getMyRecipes
from python.editRecipe.editRecipe import editRecipeData, editRecipePost
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

    # Get all recipe categories, all ingredients categories and all ingredients from Mongo and sort them alphabetically
    ingCatsDB = list(mongo.db.ingredientCategories.find())
    ingCatsDBSort = (sorted(ingCatsDB, key=lambda x: x["name"]))
    recCatsDB = list(mongo.db.recipeCategories.find())
    recCatsDBSort = (sorted(recCatsDB, key=lambda x: x["name"]))
    ingsDB = list(mongo.db.ingredients.find())
    ingsDBSort = (sorted(ingsDB, key=lambda x: x["name"]))

    return render_template("pages/add_recipe/add_recipe.html",
                            ingCats=ingCatsDBSort,
                            recCats=recCatsDBSort,
                            ings=ingsDBSort)


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


@app.route("/cookbook")
def cookbook():
    # python > cookbook > getFavRecipes.py
    userFavRecs = getFavRecipes()
    # python > cookbook > getMyRecipes.py
    userMyRecs = getMyRecipes()

    return render_template("pages/cookbook/cookbook.html",
                           favRecs=list(userFavRecs),
                           myRecs=list(userMyRecs))


@app.route("/deleteRecipe/<rec_id>")
def deleteRecipe(rec_id):
    rec = mongo.db.recipes.find_one({"_id": ObjectId(rec_id)})
    mongo.db.recipes.remove({"_id": ObjectId(rec_id)})

    return redirect(url_for("browse"))


@app.route("/editRecipe/<rec_id>", methods=["GET", "POST"])
def editRecipe(rec_id):
    if request.method == "POST":
        # python > editRecipe > editRecipe.py
        editRecipePost(rec_id)

        return redirect(url_for("viewRecipe", rec_id=rec_id))

    # python > viewRecipe > viewRecipe.py
    data = editRecipeData(rec_id)
    recDB = data[0]
    ings = data[1]
    recCats = data[2]

    # Get all recipe categories, all ingredients categories and all ingredients from Mongo
    ingCatsDB = list(mongo.db.ingredientCategories.find())
    recCatsDB = list(mongo.db.recipeCategories.find())
    ingsDB = list(mongo.db.ingredients.find())

    return render_template("pages/edit_recipe/edit_recipe.html",
                            ingCats=ingCatsDB,
                            recCatsAll=recCatsDB,
                            ingsAll=ingsDB,
                            rec=recDB,
                            ingsRec=ings,
                            recCatsRec=recCats)


@app.route("/fav/<rec_id>")
def isFav(rec_id):
    user = mongo.db.users.find_one({"_id": ObjectId("624715013b6773d36014fcbc")})

    # If recipe is already on favs, remove it
    if ObjectId(rec_id) in user["isFav"]:
        mongo.db.users.update_one({"_id": ObjectId("624715013b6773d36014fcbc")},
                                  {'$pull': {"isFav": ObjectId(rec_id)}})
    # Otherwise add it to favs
    else:
        mongo.db.users.update_one({"_id": ObjectId("624715013b6773d36014fcbc")},
                                  {'$push': {"isFav": ObjectId(rec_id)}})

    return redirect(url_for("cookbook"))


@app.route("/menu/<rec_id>")
def isMenu(rec_id):
    # Find Zoe the user
    user = mongo.db.users.find_one({"_id": ObjectId("624715013b6773d36014fcbc")})
    # Find Zoe's menu recipes
    userMenuRecs = user["isMenu"]

    # Create blank array to be populated with IDs of recipes of user menu
    userMenuRecsIds = []
    for rec in userMenuRecs:
        userMenuRec_id = rec["id"]
        userMenuRecsIds.append(userMenuRec_id)

    # Define object to be removed from menu
    userMenuRecDBPull = {
        "id": ObjectId(rec_id)
    }

    # Define object to be added to menu
    userMenuRecDBPush = {
        "id": ObjectId(rec_id),
        "serves": 4
    }

    # If recipe is already on menu, remove it
    if ObjectId(rec_id) in userMenuRecsIds:
        mongo.db.users.update_one({"_id": ObjectId("624715013b6773d36014fcbc")},
                                  {'$pull': {"isMenu": userMenuRecDBPull}})
    # Otherwise add it to menu
    else:
        mongo.db.users.update_one({"_id": ObjectId("624715013b6773d36014fcbc")},
                                  {'$push': {"isMenu": userMenuRecDBPush}})

    return redirect(url_for("menu"))


@app.route("/clearMenu", methods=["GET", "POST"])
def clearMenu():
    user = mongo.db.users.find_one({"_id": ObjectId("624715013b6773d36014fcbc")})
    userMenuRecs = user["isMenu"]

    if request.method == "POST":
        mongo.db.users.update({"_id": ObjectId("624715013b6773d36014fcbc")},
                              {'$set': {'isMenu': [] }})

        return redirect(url_for("menu"))


@app.route("/updateMenu", methods=["GET", "POST"])
def updateMenu():
    user = mongo.db.users.find_one({"_id": ObjectId("624715013b6773d36014fcbc")})
    userMenuRecs = user["isMenu"]

    if request.method == "POST":
        mongo.db.users.update({"_id": ObjectId("624715013b6773d36014fcbc")},
                              {'$set': {'isMenu': [] }})

        for index, rec in enumerate(userMenuRecs):
            userMenuRecId = request.form.get(f'id-{index+1}')
            userMenuRecServes = request.form.get(f'serves-{index+1}')
            userMenuRec = {
                "id": ObjectId(userMenuRecId),
                "serves": int(userMenuRecServes)
            }
            mongo.db.users.update_one({"_id": ObjectId("624715013b6773d36014fcbc")},
                                      {'$push': {"isMenu": userMenuRec}})

        return redirect(url_for("menu"))


@app.route("/menu")
def menu():
    # Find user and all recipe ObjectIds on their menu
    user = mongo.db.users.find_one({"_id": ObjectId("624715013b6773d36014fcbc")})
    userMenuRecs = user["isMenu"]

    # Set empty arrays for menu recipe ids, names, images and serving numbers; shopping list ingredient names, numbers and units
    userMenuRecsIds = []
    userMenuRecsNames = []
    userMenuRecsImages = []
    userMenuRecsServes = []
    userShoppingIngNames = []
    userShoppingIngCats = []
    userShoppingIngNums = []
    userShoppingIngUnits = []

    # Add menu and shopping list information into empty arrays
    for rec in userMenuRecs:
        userMenuRec = mongo.db.recipes.find_one({"_id": ObjectId(rec["id"])})

        # Menu recipes
        userMenuRec_id = rec["id"]
        userMenuRec_serves = int(rec["serves"])
        userMenuRec_name = userMenuRec["name"]
        userMenuRec_image = userMenuRec["image"]

        userMenuRecsIds.append(userMenuRec_id)
        userMenuRecsNames.append(userMenuRec_name)
        userMenuRecsImages.append(userMenuRec_image)
        userMenuRecsServes.append(userMenuRec_serves)

        # Shopping list
        userMenuRec_ingNames = userMenuRec["ingredientName"]
        userMenuRec_ingNums = userMenuRec["ingredientNum"]
        userMenuRec_ingUnits = userMenuRec["ingredientUnit"]

        # Get array of all ingredients in shopping list (duplicates)
        for ingName in userMenuRec_ingNames:
            ingNameDB = mongo.db.ingredients.find_one({"_id": ingName})["name"]
            userShoppingIngNames.append(ingNameDB)

            ingCatIdDB = mongo.db.ingredients.find_one({"_id": ingName})["category"]
            ingCatDB = mongo.db.ingredientCategories.find_one({"_id": ingCatIdDB})["name"]
            userShoppingIngCats.append(ingCatDB)

        for ingNum in userMenuRec_ingNums:
            userShoppingIngNums.append((ingNum*userMenuRec_serves))

        for ingUnit in userMenuRec_ingUnits:
            userShoppingIngUnits.append(ingUnit)

    # Add duplicate shopping list values together
    userShoppingIngNamesEdit = []
    userShoppingIngCatsEdit = []
    userShoppingIngNumsEdit = []
    userShoppingIngUnitsEdit = []
    i = 0
    imax = len(userShoppingIngNames)

    while i < imax:
        userShoppingIngName = userShoppingIngNames[i]
        userShoppingIngCat = userShoppingIngCats[i]
        userShoppingIngNum = userShoppingIngNums[i]
        userShoppingIngUnit = userShoppingIngUnits[i]

        # If the ingredient is already in the shopping list...
        if userShoppingIngName in userShoppingIngNamesEdit:
            # Find index of matching ingredient name
            index = userShoppingIngNamesEdit.index(userShoppingIngName)

            # Find categories, quantities and units of matching ingredients
            catOne = userShoppingIngCatsEdit[index]
            catTwo = userShoppingIngCat
            numOne = int(userShoppingIngNumsEdit[index])
            numTwo = int(userShoppingIngNum)
            unitOne = userShoppingIngUnitsEdit[index]
            unitTwo = userShoppingIngUnit

            # If the units of the two matching ingredients are the same, sum the quantities and don't add ingredients name to list
            if unitOne == unitTwo:
                userShoppingIngNumsEdit[index] = numOne + numTwo
            # If the units of the two matching ingredients are not the same, do not sum the quantities and add ingredients name to list
            else:
                userShoppingIngNamesEdit.append(userShoppingIngName)
                userShoppingIngCatsEdit.append(userShoppingIngCat)
                userShoppingIngNumsEdit.append(userShoppingIngNum)
                userShoppingIngUnitsEdit.append(userShoppingIngUnit)
            i += 1
        # If ingredient name is not on list of menu ingredients names add ingredients name to list
        else:
            userShoppingIngNamesEdit.append(userShoppingIngName)
            userShoppingIngCatsEdit.append(userShoppingIngCat)
            userShoppingIngNumsEdit.append(userShoppingIngNum)
            userShoppingIngUnitsEdit.append(userShoppingIngUnit)
            i += 1

    # Count ingredients of specific categories
    userShoppingIngCatsCount = {"Meat": 0,
                                "Fish": 0, 
                                "Fruit": 0, 
                                "Veg": 0, 
                                "Dairy": 0, 
                                "Cupboard": 0, 
                                "Sweets": 0, 
                                "Herbs and Spices": 0, 
                                "Booze": 0,
                                "House": 0
                                }
    userShoppingIngCatsUpdate = {i:userShoppingIngCatsEdit.count(i) for i in userShoppingIngCatsEdit}
    userShoppingIngCatsCount.update(userShoppingIngCatsUpdate)

    userMenuRecs = zip(userMenuRecsIds,
                       userMenuRecsNames,
                       userMenuRecsImages,
                       userMenuRecsServes)

    userShoppingList = zip(userShoppingIngNamesEdit,
                           userShoppingIngCatsEdit,
                           userShoppingIngNumsEdit,
                           userShoppingIngUnitsEdit)

    return render_template("pages/menu/menu.html",
                           menuRecs=list(userMenuRecs),
                           shoppingList=list(userShoppingList),
                           ingCatsCount=userShoppingIngCatsCount
                           )


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        # Get query text from user search
        query = request.form.get("query")

        # Search recipes
        searchRecipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))

    return render_template("pages/browse_recipe/browse_recipe.html",
                            recs=searchRecipes)


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