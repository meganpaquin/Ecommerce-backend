from flask import Flask, request, abort
import json, random
from data import me
from data import catalog

app = Flask(__name__)

# add the server commands first

@app.get("/")  #decorator for the root file runs home() when root loads
def home():
    return "Hello from flask"

@app.get("/test")
def test():
    return "This is another page"

@app.get("/about")
def about():
    return "Megan Paquin"    

### This part is API Products

@app.get("/api/test")
def test_api():
    return json.dumps("OK")


@app.get("/api/about")
def about_api():
    return json.dumps(me)

@app.get("/api/catalog")
def get_catalog():
    # return the list of products
    return json.dumps(catalog)

@app.post("/api/catalog")
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

    if product["price"] < 1:
        return abort(400, 'ERROR: price is less than $1')

    # you should assign a unique _id
    product["_id"] = random.randint(100000,999999)
    catalog.append(product)

    return product

@app.get('/api/product/<id>')
def get_product_byid(id):
    # the two id names must match above
    for prod in catalog:
        if prod["_id"] == str(id):
            return json.dumps(prod)
    return 'No item exists'

@app.get('/api/products/<category>')
def get_by_category(category):
    results = []
    for prod in catalog:
        if prod["category"].lower() == category.lower():
            results.append(prod)

    return json.dumps(results)

@app.get("/api/count") 
def catalog_count():
    # return the number of items in a list
    number = len(catalog)
    return json.dumps(number)

@app.get("/api/catalog/total")
def total_inventory_price():
    total = 0
    for price in catalog:
        total += price["price"]

    return json.dumps(total)

@app.get("/api/catalog/cheap")
def cheapest():
    holder = catalog[0]
    for price in catalog:
        if price["price"] < holder["price"]:
            holder = price
    
    return json.dumps(holder)
            
@app.post("/api/game")
def game():
    data = request.get_json()
    user = data.lower()
    number = random.randint(1,3)
    computer = " "
    winner = " "

    #validate input
    if user != "scissor" and user != "paper" and user != "rock":
        return abort(400, "ERROR: Please select rock, paper, or scissor")      

    #generate computer answer
    if number == 1:
        computer = "Rock"
    elif number == 2:
        computer = "Paper"
    else:
        computer = "Scissor"
    
    #determine winner
    if user == "rock":
        if computer == "Paper":
            winner = "Better Luck Next Time!"
        elif computer == "Scissor":
            winner = "You Won!"
        else:
            winner = "It's a Draw!"
    elif user == "paper":
        if computer == "Paper":
            winner = "It's a Draw!"
        elif computer == "Scissor":
            winner = "Better Luck Next Time!"
        else:
            winner = "You Won!"
    elif user == "scissor":
        if computer == "Paper":
            winner = "You Won!"
        elif computer == "Scissor":
            winner = "It's a Draw!"
        else:
            winner = "Better Luck Next Time!"
   
    #create the output
    output = {
        "User" : user.capitalize(),
        "Computer": computer,
        "Winner": winner
    }

    return json.dumps(output)
