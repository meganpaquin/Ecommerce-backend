from flask import Flask
import json
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
            
