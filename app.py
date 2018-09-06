import os
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
from scrape_mars import scrape

MONGO_URL = "mongodb://localhost:27017/app"

client = MongoClient(MONGO_URL)
# db = client.app105690057
db = client.mars
collection = db.scraped

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URL

# app.config["MONGO_URI"] = "mongodb://localhost:27017/app"
# app.config["MONGO_URI"] = "mongodb://localhost:27017/app"
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)


# conn = "mongodb://localhost:27017/mars"
# conn = "mongodb://localhost:27017"
# client = MongoClient(conn)
# collections = db.scraped
# collections = mongo.db.scraped


@app.route("/")
def home():
    mars_data = mongo.db.mars.find_one()
    # mars_data = collection.find_one()
    return render_template("index.html", mars_data=mars_data)

# Route to trigger scrape function
@app.route("/scrape")
def scraper():
    new_mars_data = scrape()
    # collection.insert_one(new_mars_data)
    mongo.db.mars.insert_one(new_mars_data)
    return redirect('/')


if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)