from flask import Flask, render_template, request
from scraper import scrape_data, save_to_csv, data_processing, mongoDB
from search import search_clubs
from visualization import generate_visualizations
from pymongo import MongoClient

 
# Create the Flask app
app = Flask(__name__, template_folder='templates')

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['football']
collection = db['ranking']


# Create the routes
@app.route('/')
def index():
    return render_template('index.html')


# Scrape the data and store it in a MongoDB collection
def scrape():
    data = scrape_data()
    save_to_csv(data)
    data_processing()
    mongoDB()
    return 'Scraped and stored data successfully!'


# Search for a club
@app.route('/search', methods=['GET', 'POST']) 
def search():
    
    results = None
    
    # If the request method is POST, we get the query from the form
    if request.method == 'POST':
        query = request.form['query']

        tricroissant = request.form.get('tri_croissant', False) # We get the value of the checkbox 
        tridecroissant = request.form.get('tri_decroissant', False) # We get the value of the checkbox
        
        # If the checkbox is checked, we sort the results in ascending order
        if request.form.get('match_played_only'):
            results = search_clubs(query, match_played_only=True, tri_croissant= tricroissant, tri_decroissant = tridecroissant )
        elif request.form.get('goal_scored_only'): # If the checkbox is checked, we sort the results in descending order
            results = search_clubs(query, goal_scored_only=True, tri_croissant= tricroissant, tri_decroissant = tridecroissant)
        elif request.form.get('position_only'): # If the checkbox is checked, we sort the results in descending order
            results = search_clubs(query, position_only=True, tri_croissant= tricroissant, tri_decroissant = tridecroissant)
        else:
            results = search_clubs(query)
   
    return render_template('search.html', results=results)


# Visualize the data
@app.route('/visualize')
def visualize():
    generate_visualizations()
    return render_template('visualize.html')


# Run the app
if __name__ == '__main__':
    scrape()
    app.run()