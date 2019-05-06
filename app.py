from flask import Flask, render_template, redirect
#from flask_pymongo import PyMongo
import scrape_mars
import pymongo

app = Flask(__name__)

# Or set inline
#mongo = PyMongo(app, uri="mongodb://localhost:27017")

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.mars_info

@app.route("/")
def index():
    mars_info = db.mars_info.find_one()
    # print(mars_info)
    # print ('here')
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scraper():
    mars_info = db.mars_info
    mars_data = scrape_mars.scrape()
    mars_info.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
