from flask import Flask
import json
from data import me

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


app.run(debug=True)
# This is starting the server... this should be the last thing on the file
# remove debug for production
