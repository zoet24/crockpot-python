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
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env
import random
from python.addRecipe.addRecipe import addRecipePost
from python.cookbook.getFavRecipes import getFavRecipes
from python.cookbook.getMyRecipes import getMyRecipes
from python.editRecipe.editRecipe import editRecipeData, editRecipePost
from python.utility.findFavMenu import findFavMenu
from python.viewRecipe.viewRecipe import viewRecipeData


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("pages/index/index.html")


# ACCOUNT FUNCTIONS
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if username exists in db
        existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

        if existing_user:
            # Check hashed password matches user input
            if check_password_hash(existing_user["password"], request.form.get("password")):
                # Add user to session cookie
                session["user"] = request.form.get("username").lower()
                flash("Welcome back " + session["user"] + "!")
                return redirect(url_for("cookbook"))
            else:
                # Invalid password match
                flash("Sorry, we can't find an account with those details.")
                return redirect(url_for("login"))
        else:
            # Username doesn't exist
            flash("Sorry, we can't find an account with those details.")
            return redirect(url_for("login"))

    return render_template("pages/login/login.html")


@app.route("/logout")
def logout():
    # Remove user from session cookie
    flash("See you later " + session["user"] + "!")
    session.pop("user")

    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Check if username exists in db
        existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

        if existing_user:
            flash("This username already exists!")
            return redirect(url_for("signup"))

        signup = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "isFav": [],
            "isMenu": [],
            "isShopping": [],
        }

        mongo.db.users.insert_one(signup)

        # Put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Welcome " + session["user"] + "!")
        return redirect(url_for("cookbook"))

    return render_template("pages/signup/signup.html")


# DATABASE FUNCTIONS
@app.route("/addRecipe", methods=["GET", "POST"])
def addRecipe():
    isSession = session.get("user")

    if not isSession:
        return redirect(url_for("browse"))

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

    # Find all ingredients excluding house category
    ingsDB = list(mongo.db.ingredients.find({ "category": { '$ne': ObjectId('627b77eab0cda8e4664c18bf') } }))
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
    flash(ingDB["name"] + " (" + request.form.get("category").title() + ") has been added to your ingredients.")

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
    flash(catDB["name"] + " has been added to your categories.")

    return redirect(url_for("addRecipe"))


@app.route("/browse")
def browse():
    isSession = session.get("user")

    # Get all recipes from Mongo db
    recsDB = list(mongo.db.recipes.find())
    random.shuffle(recsDB)

    # Get all recipe categories and all ingredients from Mongo and sort them alphabetically
    recCatsDB = list(mongo.db.recipeCategories.find())
    recCatsDBSort = (sorted(recCatsDB, key=lambda x: x["name"]))
    ingsDB = list(mongo.db.ingredients.find({ "category": { '$ne': ObjectId('627b77eab0cda8e4664c18bf') } }))
    ingsDBSort = (sorted(ingsDB, key=lambda x: x["name"]))

    if isSession:
        isFav = findFavMenu()[0]
        isMenu = findFavMenu()[1]
    else:
        isFav = []
        isMenu = []

    return render_template("pages/browse_recipe/browse_recipe.html",
                            recs=recsDB,
                            recCats=recCatsDBSort,
                            ings=ingsDBSort,
                            isFav=isFav,
                            isMenu=isMenu)


@app.route("/cookbook")
def cookbook():
    isSession = session.get("user")

    if not isSession:
        return redirect(url_for("browse"))

    # python > cookbook > getFavRecipes.py
    userFavRecs = list(getFavRecipes())
    random.shuffle(userFavRecs)
    # python > cookbook > getMyRecipes.py
    userMyRecs = list(getMyRecipes())
    random.shuffle(userMyRecs)

    isFav = findFavMenu()[0]
    isMenu = findFavMenu()[1]

    return render_template("pages/cookbook/cookbook.html",
                           isFav=isFav,
                           isMenu=isMenu,
                           favRecs=userFavRecs,
                           myRecs=userMyRecs)


@app.route("/deleteRecipe/<rec_id>")
def deleteRecipe(rec_id):
    rec = mongo.db.recipes.find_one({"_id": ObjectId(rec_id)})
    user = mongo.db.users.find_one({"username": session["user"]})

    # Check to see if current user created recipe
    if user["_id"] == rec["user"]:
        flash(rec["name"] + " has been deleted from your recipes.")
        mongo.db.recipes.remove({"_id": ObjectId(rec_id)})
    else:
        flash("You can't delete " + rec["name"])

    return redirect(url_for("browse"))


@app.route("/editRecipe/<rec_id>", methods=["GET", "POST"])
def editRecipe(rec_id):
    rec = mongo.db.recipes.find_one({"_id": ObjectId(rec_id)})
    user = mongo.db.users.find_one({"username": session["user"]})

     # Check to see if current user created recipe
    if user["_id"] != rec["user"]:
        flash("You can't edit " + rec["name"])
        return redirect(url_for("browse"))

    if request.method == "POST":
        # python > editRecipe > editRecipe.py
        editRecipePost(rec_id)
        flash(rec["name"] + " has been updated.")

        return redirect(url_for("viewRecipe", rec_id=rec_id))

    # python > viewRecipe > viewRecipe.py
    data = editRecipeData(rec_id)
    recDB = data[0]
    ings = data[1]
    recCats = data[2]

    # Get all recipe categories, all ingredients categories and all ingredients from Mongo and sort them alphabetically
    ingCatsDB = list(mongo.db.ingredientCategories.find())
    ingCatsDBSort = (sorted(ingCatsDB, key=lambda x: x["name"]))
    recCatsDB = list(mongo.db.recipeCategories.find())
    recCatsDBSort = (sorted(recCatsDB, key=lambda x: x["name"]))
    ingsDB = list(mongo.db.ingredients.find({ "category": { '$ne': ObjectId('627b77eab0cda8e4664c18bf') } }))
    ingsDBSort = (sorted(ingsDB, key=lambda x: x["name"]))

    return render_template("pages/edit_recipe/edit_recipe.html",
                            ingCats=ingCatsDBSort,
                            recCatsAll=recCatsDBSort,
                            ingsAll=ingsDBSort,
                            rec=recDB,
                            ingsRec=ings,
                            recCatsRec=recCats)


@app.route("/fav/<rec_id>")
def isFav(rec_id):
    rec = mongo.db.recipes.find_one({"_id": ObjectId(rec_id)})
    user = mongo.db.users.find_one({"username": session["user"]})

    # If recipe is already on favs, remove it
    if ObjectId(rec_id) in user["isFav"]:
        mongo.db.users.update_one({"_id": ObjectId(user["_id"])},
                                  {'$pull': {"isFav": ObjectId(rec_id)}})
        flash(rec["name"] + " has been removed from your favourites.")

    # Otherwise add it to favs
    else:
        mongo.db.users.update_one({"_id": ObjectId(user["_id"])},
                                  {'$push': {"isFav": ObjectId(rec_id)}})
        flash(rec["name"] + " has been added to your favourites.")

    return redirect(url_for("cookbook"))


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        # Get all recipes from db
        recsDB = list(mongo.db.recipes.find())

        # Get query text from user search
        query = request.form.get("query").split('&')

        # Search for name
        queryRec = query[0]
        searchRecsNames = list(mongo.db.recipes.find({"$text": {"$search": f"\"{queryRec}\""}}))
        searchRecsNamesIds = []
        for rec in searchRecsNames:
            searchRecsNamesIds.append(rec['_id'])

        # Search for ingredients
        queryIngs = query[1].rstrip().split(' ')
        searchRecsIngsIds = []
        for rec in recsDB:
            isMatch = all(item in rec['ingredientTags'].rstrip().split(' ') for item in queryIngs)
            if isMatch:
                searchRecsIngsIds.append(rec['_id'])

        # Search for categories
        queryCats = query[2].rstrip().split(' ')
        searchRecsCatsIds = []
        for rec in recsDB:
            isMatch = all(item in rec['categoryTags'].rstrip().split(' ') for item in queryCats)
            if isMatch:
                searchRecsCatsIds.append(rec['_id'])

        searchRecsIds = []

        if (len(searchRecsNamesIds) > 0):
            searchRecsIds = searchRecsNamesIds
        if (len(searchRecsIngsIds) > 0):
            searchRecsIds = searchRecsIngsIds
        if (len(searchRecsCatsIds) > 0):
            searchRecsIds = searchRecsCatsIds
        if (len(searchRecsNamesIds) > 0) and (len(searchRecsIngsIds) > 0):
            searchRecsIds = (set(searchRecsNamesIds) & set(searchRecsIngsIds))
        if (len(searchRecsNamesIds) > 0) and (len(searchRecsCatsIds) > 0):
            searchRecsIds = (set(searchRecsNamesIds) & set(searchRecsCatsIds))
        if (len(searchRecsIngsIds) > 0) and (len(searchRecsCatsIds) > 0):
            searchRecsIds = (set(searchRecsIngsIds) & set(searchRecsCatsIds))
        if (len(searchRecsNamesIds) > 0) and (len(searchRecsIngsIds) > 0) and (len(searchRecsCatsIds) > 0):
            searchRecsIds = (set(searchRecsNamesIds) & set(searchRecsIngsIds) & set(searchRecsCatsIds))

        searchRecs = []
        for recId in searchRecsIds:
            rec = mongo.db.recipes.find_one({"_id": ObjectId(recId)})
            searchRecs.append(rec)

        isFav = findFavMenu()[0]
        isMenu = findFavMenu()[1]

    return render_template("pages/browse_recipe/browse_recipe.html",
                            recs=searchRecs,
                            isFav=isFav,
                            isMenu=isMenu)


@app.route("/viewRecipe/<rec_id>")
def viewRecipe(rec_id):
    isSession = session.get("user")

    # python > viewRecipe > viewRecipe.py
    data = viewRecipeData(rec_id)
    recDB = data[0]
    ings = data[1]
    recCat_names = data[2]
    user = data[3]

    if isSession:
        isFav = findFavMenu()[0]
        isMenu = findFavMenu()[1]
    else:
        isFav = []
        isMenu = []

    return render_template("pages/view_recipe/view_recipe.html",
                           rec=recDB,
                           ings=ings,
                           recCats=recCat_names,
                           user=user,
                           isFav=isFav,
                           isMenu=isMenu)


# MENU FUNCTIONS
@app.route("/menu/<rec_id>/<serves>")
def isMenu(rec_id, serves):
    # Find the user
    user = mongo.db.users.find_one({"username": session["user"]})
    # Find the user's menu recipes
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
        "serves": serves
    }

    # If recipe is already on menu, remove it
    if ObjectId(rec_id) in userMenuRecsIds:
        rec = mongo.db.recipes.find_one({"_id": ObjectId(rec_id)})
        mongo.db.users.update_one({"_id": ObjectId(user["_id"])},
                                  {'$pull': {"isMenu": userMenuRecDBPull}})
        flash(rec["name"] + " has been removed from your menu.")
    # Otherwise add it to menu
    else:
        rec = mongo.db.recipes.find_one({"_id": ObjectId(rec_id)})
        mongo.db.users.update_one({"_id": ObjectId(user["_id"])},
                                  {'$push': {"isMenu": userMenuRecDBPush}})
        flash(rec["name"] + " has been added to your menu.")

    return redirect(url_for("menu"))


@app.route("/clearMenu", methods=["GET", "POST"])
def clearMenu():
    user = mongo.db.users.find_one({"username": session["user"]})
    userMenuRecs = user["isMenu"]
    userShopping = user["isShopping"]

    if request.method == "POST":
        mongo.db.users.update({"_id": ObjectId(user["_id"])},
                              {'$set': {'isMenu': [] }})
        mongo.db.users.update({"_id": ObjectId(user["_id"])},
                              {'$set': {'isShopping': [] }})
        flash("Your menu has been cleared.")

        return redirect(url_for("menu"))


@app.route("/updateMenu", methods=["GET", "POST"])
def updateMenu():
    user = mongo.db.users.find_one({"username": session["user"]})
    userMenuRecs = user["isMenu"]

    if request.method == "POST":
        mongo.db.users.update({"_id": ObjectId(user["_id"])},
                              {'$set': {'isMenu': [] }})
        flash("Your menu has been updated.")

        for index, rec in enumerate(userMenuRecs):
            userMenuRecId = request.form.get(f'id-{index+1}')
            userMenuRecServes = request.form.get(f'serves-{index+1}')
            userMenuRec = {
                "id": ObjectId(userMenuRecId),
                "serves": int(userMenuRecServes)
            }
            mongo.db.users.update_one({"_id": ObjectId(user["_id"])},
                                      {'$push': {"isMenu": userMenuRec}})

        return redirect(url_for("menu"))


@app.route("/menu")
def menu():
    isSession = session.get("user")

    if not isSession:
        return redirect(url_for("browse"))

    # Find user and all recipe ObjectIds on their menu
    user = mongo.db.users.find_one({"username": session["user"]})
    userMenuRecs = user["isMenu"]
    userShopping = user["isShopping"]

    isFav = findFavMenu()[0]
    isMenu = findFavMenu()[1]

    ingsDB = list(mongo.db.ingredients.find())
    ingsDBSort = (sorted(ingsDB, key=lambda x: x["name"]))

    # Set empty arrays for menu recipe ids, names, images and serving numbers; shopping list ingredient names, numbers and units
    userMenuRecsIds = []
    userMenuRecsNames = []
    userMenuRecsImages = []
    userMenuRecsServes = []
    userShoppingList = []
    userShoppingIngNames = []
    userShoppingIngCats = []
    userShoppingIngNums = []
    userShoppingIngUnits = []
    userShoppingIngNamesExtra = []

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

        # Get array of all ingredients from menu in shopping list (duplicates)
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

    # Get array of all ingredients from shopping list in shopping list (duplicates)
    for shopping in userShopping:
        userShopping_ingName = shopping["ingredientName"]
        userShopping_ingNum = shopping["ingredientNum"]
        userShopping_ingUnit = shopping["ingredientUnit"]

        # Add name of ingredients
        ingNameDB = mongo.db.ingredients.find_one({"_id": userShopping_ingName})["name"]
        userShoppingIngNames.append(ingNameDB)

        if shopping["ingredientNum"] > 0:
            userShoppingIngNamesExtra.append(ingNameDB)

        # Add category
        ingCatIdDB = mongo.db.ingredients.find_one({"_id": userShopping_ingName})["category"]
        ingCatDB = mongo.db.ingredientCategories.find_one({"_id": ingCatIdDB})["name"]
        userShoppingIngCats.append(ingCatDB)

        # Add quantity
        userShoppingIngNums.append(userShopping_ingNum)

        # Add unit
        userShoppingIngUnits.append(userShopping_ingUnit)

    # Add duplicate shopping list values together and remove < 0 values
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

    # # Alphabetise shopping list
    j = 0
    jmax = len(userShoppingIngNamesEdit) - 1
    userShoppingList = []

    while j <= jmax:
        userShoppingList.append([userShoppingIngNamesEdit[j],
                                 userShoppingIngCatsEdit[j],
                                 userShoppingIngNumsEdit[j],
                                 userShoppingIngUnitsEdit[j]
                                ])
        j += 1

    userShoppingList = (sorted(userShoppingList, key=lambda x: x[0]))
    userShoppingIngNamesExtra = (sorted(userShoppingIngNamesExtra, key=lambda x: x[0]))

    # Count ingredients of specific categories
    userShoppingIngCatsCount = {"Meat": 0,
                                "Fish": 0, 
                                "Fruit": 0, 
                                "Veg": 0, 
                                "Dairy": 0, 
                                "Cupboard": 0, 
                                "Sweets": 0, 
                                "Herbs and Spices": 0, 
                                "Drinks": 0,
                                "House": 0
                                }
    userShoppingIngCatsUpdate = {i:userShoppingIngCatsEdit.count(i) for i in userShoppingIngCatsEdit}
    userShoppingIngCatsCount.update(userShoppingIngCatsUpdate)

    userMenuRecs = zip(userMenuRecsIds,
                       userMenuRecsNames,
                       userMenuRecsImages,
                       userMenuRecsServes)

    return render_template("pages/menu/menu.html",
                           isFav=isFav,
                           isMenu=isMenu,
                           menuRecs=list(userMenuRecs),
                           shoppingList=userShoppingList,
                           shoppingExtra=userShoppingIngNamesExtra,
                           ingCatsCount=userShoppingIngCatsCount,
                           ings=ingsDBSort
                           )


# SHOPPING LIST FUNCTIONS
@app.route("/addShopping", methods=["GET", "POST"])
def addShopping():
    if request.method == "POST":
        user = mongo.db.users.find_one({"username": session["user"]})

        shoppingListIng= {
            "ingredientName": ObjectId(request.form.get("ingredientName")),
            "ingredientNum": float(request.form.get("ingredientNum")),
            "ingredientUnit": request.form.get("ingredientUnit")
        }

        mongo.db.users.update_one({"_id": ObjectId(user["_id"])},
                                  {'$push': {"isShopping": shoppingListIng}})

    return redirect(url_for("menu"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) # Change to false on deploy