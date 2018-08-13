from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/app"

mongo = PyMongo(app)


@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    print(mars_data)
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    mars_info = scrape_mars.scrape()
    print(mars_info)
    mars_data.update(
        {},
        mars_info,
        upsert=True
    )
    return redirect("/", code=302)

if __name__=="__main__":
    app.run()