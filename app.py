from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

#Create an instance of Flask
app = Flask(__name__)

#Use PyMongo to establish Mongo connection
#Local MongoDB connection
mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_db')

#Create route that renders index.html template using data from Mongo
@app.route("/")
def index():

    #Get data from MongoDB
    destination_data = mongo.db.collection.find_one()
        
    #Return template and data
    return render_template("index.html", mars=destination_data)

#Import python function from scrape_mars.py
#from scrape_mars import mars_scrape

#Route that will trigger scrape function
@app.route("/scrape")
def scrape():

    #Run the scrape function
    mars_dict = scrape_mars.mars_scrape()

    #Insert into database
    mongo.db.collection.update({}, mars_dict, upsert=True)

    #coll.update({'id': 1}, {'$set': mars_mission_data}, upsert=True)

    #Redirect back to homepage
    return redirect("/")
    

if __name__ == "__main__":
    app.run(debug=True)