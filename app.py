from flask import Flask, render_template, jsonify, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/app"

mongo = PyMongo(app)

# Route to render index.html
@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

# Route to trigger scrape function
@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    mars_info = scrape_mars.scrape()
    mars_data.update(
        {},
        mars_info,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)
    # return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)