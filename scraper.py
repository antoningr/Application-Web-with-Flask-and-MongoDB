import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from pymongo import MongoClient


# scrape_data() : Scrape data from the Wikipedia page
def scrape_data():
    
    # Get the HTML content of the Wikipedia page
    url = 'https://fr.wikipedia.org/wiki/Classement_du_championnat_de_France_de_football_toutes_saisons_confondues'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable'})

    # Get the table headers
    headers = [th.text.strip() for th in table.find_all('th')]

    # Initialize the list of rows
    rows = []
    
    # Get the table rows
    for tr in table.tbody.find_all('tr'):
        if tr.find('th') is None:
            # Get the row data and append it to the list of rows
            row = [td.text.strip() for td in tr.find_all('td')]
            if len(row) == len(headers):
                rows.append(row)

    # Create a dictionary with the headers and rows
    data = {'headers': headers, 'rows': rows}
    return data


# save_to_csv() : Save the data to a CSV file
def save_to_csv(data):
    with open('data_brut.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data['headers'])
        writer.writerows(data['rows'])


# data_processing() : Process the data
def data_processing():
    
    # Read the CSV file into a pandas dataframe
    data = pd.read_csv('data_brut.csv', encoding='ISO-8859-1')

    # Rename the columns
    data.columns = ['Position', 'Club', 'Saison', 'Match_Joue', 'Match_Gagne', 'Match_Nul', 'Match_Perdu', 'But_Pour', 'But_Contre', 'Difference', 'Points_Totals', 'Derniere_Saison', 'Championnat_Actuel', 'Titres_Totales']
    
    # Fill the NaN values in the 'Derniere_Saison' and 'Championnat_Actuel' columns
    data['Derniere_Saison'].fillna('Club actuellement en Ligue 1', inplace=True)
    data.loc[data['Derniere_Saison'] == 'Club actuellement en Ligue 1', 'Championnat_Actuel'] = data.loc[data['Derniere_Saison'] == 'Club actuellement en Ligue 1', 'Championnat_Actuel'].fillna('Ligue 1')
    data['Championnat_Actuel'].fillna('Club disparu', inplace=True)

    # Replace the special characters in the 'Club', 'Derniere_Saison' and 'Championnat_Actuel' columns
    data['Club'] = data['Club'].str.replace('Ã©', 'e').str.replace('Ã¨', 'e').str.replace('Ãª', 'e').str.replace('Ã¢', 'a').str.replace('Ã®', 'i').str.replace('Ã§', 'c').str.replace('Ã', 'E')
    data['Derniere_Saison'] = data['Derniere_Saison'].str.replace('Ã©', 'e').str.replace('Ã¨', 'e').str.replace('Ãª', 'e').str.replace('Ã¢', 'a').str.replace('Ã®', 'i').str.replace('Ã§', 'c').str.replace('Ã', 'E')
    data['Championnat_Actuel'] = data['Championnat_Actuel'].str.replace('Ã©', 'e').str.replace('Ã¨', 'e').str.replace('Ãª', 'e').str.replace('Ã¢', 'a').str.replace('Ã®', 'i').str.replace('Ã§', 'c').str.replace('Ã', 'E')

    # Replace the special characters in the 'Championnat_Actuel' column
    data["Championnat_Actuel"] = data["Championnat_Actuel"].str.replace(r'\(Niv \d+\)', '', regex=True)

    # Replace the special characters in the 'Championnat_Actuel' column
    data["Championnat_Actuel"] = data['Championnat_Actuel'].replace('(Inconnue)', 'District 1')

    # Convert the 'Points_Totals' and 'Titres_Totales' columns to integers
    data['Points_Totals'] = data['Points_Totals'].str.replace(' ', '').astype(int)
    data['Titres_Totales'] = data['Titres_Totales'].str.replace('*', '', regex=False).fillna(0).astype(int)

    # Create new columns in the dataframe 
    data['Pourcentage_Match_Gagne'] = data['Match_Gagne'] / data['Match_Joue']
    data['Pourcentage_Match_Nul'] = data['Match_Nul'] / data['Match_Joue']
    data['Pourcentage_Match_Perdu'] = data['Match_Perdu'] / data['Match_Joue']
    data['But_Pour_par_Match_en_Moyenne'] = data['But_Pour'] / data['Match_Joue']
    data['But_Contre_par_Match_en_Moyenne'] = data['But_Contre'] / data['Match_Joue']
    data['Difference_par_Match_en_Moyenne'] = data['Difference'] / data['Match_Joue']
    data['Points_Totals_par_Match_en_Moyenne'] = data['Points_Totals'] / data['Match_Joue']
    data['But_Pour_par_Saison_en_Moyenne'] = data['But_Pour'] / data['Saison']
    data['But_Contre_par_Saison_en_Moyenne'] = data['But_Contre'] / data['Saison']
    data['Difference_par_Saison_en_Moyenne'] = data['Difference'] / data['Saison']
    data['Points_Totals_par_Saison_en_Moyenne'] = data['Points_Totals'] / data['Saison']
    data['Pourcentage_Titres_par_Saison'] = data['Titres_Totales'] / data['Saison']

    # Save the dataframe to a CSV file
    data.to_csv('data.csv', index=False)


# mongoDB() : Save the data to a MongoDB collection
def mongoDB():

    # Connect to the MongoDB server
    client = MongoClient('localhost', 27017)
    db = client['football']
    collection = db['ranking']

    # Read the CSV file into a pandas dataframe
    with open('data.csv') as csvfile:

        # Create a dictionary reader
        reader = csv.DictReader(csvfile)
        
        # Insert the data into the collection
        for row in reader:
            collection.insert_one(row)
