from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo 
import Mission


app = Flask(__name__)


# Local MongoDB connection #

#------------------------------------------------------------------------------------#

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)
db = client.mars_db
coll = db.mars_data_coll


#------------------------------------------------------------------------------------#

@app.route("/")

def index():


    mars_mission_data = coll.find_one()
    return render_template("index.html", data=mars_mission_data)
 
# Route that will trigger scrape function.

@app.route("/scrape")

def scrape():


    mars_mission_data = Mission.scraper()

    print("in app.py")
    print(mars_mission_data)

    coll.update_many({"id": 1}, {"$set": mars_mission_data}, upsert=True)
    return redirect("/", code=302)
    # return "Scraping Successful!"

@app.route("/example")
def example():
    word = "Hello World"
    return word


if __name__ == "__main__":
    app.run(debug=True)