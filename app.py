#import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#set up Flask
app = Flask(__name__)

#use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#set up Flask routes
@app.route("/")
def index():
    mars = mongo.db.mars_app.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars_app
    mars_data = scraping.scrape_all()
    print(mars_data)
    mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

#Tell Flask to go
if __name__ == "__main__":
    app.run()
