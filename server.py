from flask import Flask, request, abort
import json
from flask_cors import CORS
from config import database
from bson import ObjectId

app = Flask(__name__)
CORS(app) # disable CORS, anyone can access this API

# fix all the strings from the database use every time you get/push data from database
def fix_id(obj):
    obj["_id"] = str(obj["_id"])
    return obj

@app.get("/")
def welcome():
    return "Welcome to the server"

@app.get("/api/catalog")
def get_catalog():
    # return the list of products
    cursor = database.Products.find({}) # read all products on the database the {} is the filter option
    results = []
    for prod in cursor:
        prod = fix_id(prod)
        results.append(prod)

    return json.dumps(results)

@app.post("/api/products")
def save_product():
    product = request.get_json()
    # validation
    if not "title" in product:
        return abort(400,"ERROR: title is required")

    if len(product["title"]) < 5:
        return abort(400, "ERROR: title is too short")

    if not "category" in product:
        return abort(400, "ERROR: category is required")

    if not "price" in product:
        return abort(400, "ERROR: price is required")

    if int(product["price"]) < 1:
        return abort(400, 'ERROR: price is less than $1')

    database.Products.insert_one(product)
    
    #fix _id formatting error from mongo
    product["_id"] = str(product["_id"])

    return json.dumps(product)

@app.get('/api/product/<id>')
def get_product_byid(id):
    # the two id names must match above
   prod = database.Products.find_one({"_id": ObjectId(id)})

   if not prod:
    return abort(404, "Product Not Found")

   prod = fix_id(prod)
   return json.dumps(prod)

@app.get('/api/products/<category>')
def get_by_category(category):
    cursor = database.Products.find({ "category": category})
    results = []

    if not category:
        return abort(404, "Category Not Found")

    for prod in cursor:
        prod = fix_id(prod)
        results.append(prod)

    return json.dumps(results)

@app.get("/api/count") 
def catalog_count():
    # return the number of items in a list
    cursor = database.Products.find({})
    count = 0
    for prod in cursor:
        count += 1

    return json.dumps(count)

@app.get("/api/catalog/total")
def total_inventory_price():
    cursor = database.Products.find({})
    total = 0
    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)

@app.get("/api/catalog/deals")
def deals():
    cursor = database.Products.find({})
    results = []

    for prod in cursor:
        if prod["price"] < 10:
            prod = fix_id(prod)
            results.append(prod)

    return json.dumps(results)



@app.get("/api/coupon")
def getCoupon():
    cursor = database.Coupons.find({})
    results = []

    for coupon in cursor:
        coupon = fix_id(coupon)
        results.append(coupon)
    return json.dumps(results)

@app.post("/api/coupon")
def saveCoupon():
    new = request.get_json()

    if not "code" in new:
        return abort(400, "ERROR: code is required")
    if not "discount" in new:
        return abort(400, "ERROR: discount required")

    database.Coupons.insert_one(new)
    new = fix_id(new)
    return json.dumps(new)


@app.post("/api/user")
def saveUser():
    user = request.get_json()

    if not "fname" in user:
        return abort(400, "ERROR: first name is required")
    if not "lname" in user:
        return abort(400, "ERROR: last name is required")
    if not "email" in user:
        return abort(400, "ERROR: email is required")
    if not "phone" in user:
        return abort(400, "ERROR: phone is required")
    if not "password1" in user:
        return abort(400, "ERROR: password is required")
    if not "password2" in user:
        return abort(400, "ERROR: password is required")
    if "password1" in user == "password2" in user:
        return abort(400, "ERROR: password is required")

    database.Users.insert_one(user)
    user = fix_id(user)
    return json.dumps(user)
  

@app.get("/api/user/<email>")
def getUser(email):
    user = database.Users.find_one({"email" : email})

    if not user:
        return abort(404, "User Not Found")
    
    user = fix_id(user)
    return json.dumps(user)

@app.post("/api/order")
def saveOrder():
    new = request.get_json()
   
    # add verification here
    if not "address":
        return abort(400, "ERROR: address is required")
    if not "city":
        return abort(400, "ERROR: city is required")
    if not "state":
        return abort(400, "ERROR: state is required")
    if not "zipcode":
        return abort(400, "ERROR: zipcode is required")
    if not "card-num":
        return abort(400, "ERROR: card number is required")
    if not "expiration":
        return abort(400, "ERROR: expiration is required")
    if not "ccv":
        return abort(400, "ERROR: CCV is required")

    # database.Orders.insert_many(new)
    new = fix_id(new)
    return json.dumps(new)