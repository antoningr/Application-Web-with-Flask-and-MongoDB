import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os


# generate_visualizations() : Generate the visualizations
def generate_visualizations():

    # Get the current working directory
    cwd = os.getcwd()

    # Specify the path to the static folder
    static_folder = os.path.join(cwd, 'static')

    # Specify the path to the images
    graph1 = os.path.join(static_folder, 'graph1.png')
    graph2 = os.path.join(static_folder, 'graph2.png')
    graph3 = os.path.join(static_folder, 'graph3.png')
    graph4 = os.path.join(static_folder, 'graph4.png')
    graph5 = os.path.join(static_folder, 'graph5.png')

    # Read the CSV file into a pandas dataframe
    data = pd.read_csv('data.csv')

    # Create the visualizations
    cgraph1(graph1, data)
    cgraph2(graph2, data)
    cgraph3(graph3, data)
    cgraph4(graph4, data)
    cgraph5(graph5, data)
    

# Create the visualizations 
def cgraph1(path, data):
    
    # Filter to only include clubs that have been in Ligue 1 for more than 15 seasons
    data = data[data['Saison'] > 15]

    # Sort the data by number of seasons in descending order
    data = data.sort_values(by='Saison', ascending=False)

    # Get the data
    Club = data['Club']
    Nb_Saison = data['Saison']
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(18,6))
    ax.bar(Club, Nb_Saison)
    ax.set_xlabel('Les clubs de football', fontsize=15)
    ax.set_ylabel('Le nombre de saison en Ligue 1', fontsize=15)
    ax.set_title("Le nombre de saison en Ligue 1 des principaux clubs de football", fontsize=20)
    for i, v in enumerate(Nb_Saison):
        ax.text(i, v + 0.5, str(v), color='black', fontweight='bold', fontsize=10, ha='center')
    plt.xticks(rotation=80, fontsize=10)

    # Save the visualization
    fig.savefig(path, bbox_inches='tight')


# Create the visualizations 
def cgraph2(path, data):

    # Filter to only include clubs that have been in Ligue 1 for more than 15 seasons
    data = data[data['Saison'] > 15]

    # Sort the data by number of seasons in descending order
    data = data.sort_values(by='But_Pour', ascending=False)

    # Get the data
    Club = data['Club']
    But_Pour = data['But_Pour']
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(18,6))
    ax.bar(Club, But_Pour)
    ax.set_xlabel('Les clubs de football', fontsize=15)
    ax.set_ylabel('Le nombre de buts', fontsize=15)
    ax.set_title("Le nombre de buts des principaux clubs dans l'histoire de la Ligue 1", fontsize=20)
    for i, v in enumerate(But_Pour):
        ax.text(i, v + 1, str(v), color='black', fontweight='bold', fontsize=10, ha='center')
    plt.xticks(rotation=80, fontsize=10)

    # Save the visualization
    fig.savefig(path, bbox_inches='tight')


# Create the visualizations
def cgraph3(path, data):

    # Filter to only include clubs that have been in Ligue 1 for more than 15 seasons
    data = data[data['Saison'] > 15]

    # Sort the data by number of seasons in descending order
    data = data.sort_values(by='Pourcentage_Match_Gagne', ascending=False)

    # Get the data
    clubs = data['Club']
    won_perc = data['Pourcentage_Match_Gagne']
    drawn_perc = data['Pourcentage_Match_Nul']
    lost_perc = data['Pourcentage_Match_Perdu']

    # Create stacked bar chart
    fig, ax = plt.subplots(figsize=(18,6))
    ax.bar(clubs, won_perc, label='Matchs gagnés')
    ax.bar(clubs, drawn_perc, bottom =won_perc, label='Matchs nul')
    ax.bar(clubs, lost_perc, bottom=won_perc+drawn_perc, label='Match perdus')
    ax.set_xlabel('Les clubs de football', fontsize=15)
    ax.set_ylabel('Les pourcentages de matchs', fontsize=15)
    ax.set_title("Comparaison des pourcentages de matchs gagnés, nul et perdus des principaux clubs", fontsize=20)
    plt.xticks(rotation=80, fontsize=10)
    
    # Save the visualization
    fig.savefig(path, bbox_inches='tight')


# Create the visualizations
def cgraph4(path, data):
    
    # Get the data
    Pourcentage_Match_Gagné = data['Pourcentage_Match_Gagne']
    But_Pour_par_Match_en_Moyenne = data['But_Pour_par_Match_en_Moyenne']

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(18,6))
    ax.scatter(But_Pour_par_Match_en_Moyenne, Pourcentage_Match_Gagné, alpha=0.5)
    ax.set_xlabel('Nombres moyens de buts par matchs', fontsize=15)
    ax.set_ylabel('Pourcentage de victoire par matchs', fontsize=15)
    ax.set_title("Comparaison entre le pourcentage de victoire et le nombres moyens de buts par matchs", fontsize=20)
    plt.xticks(fontsize=10)
    
    # Save the visualization
    fig.savefig(path, bbox_inches='tight')


# Create the visualizations
def cgraph5(path, data):
    
    # Filter out clubs with zero titles
    data = data[data['Titres_Totales'] > 0]

    # Sort the data by number of seasons in descending order
    data = data.sort_values(by='Titres_Totales', ascending=False)

    # Get total titles per club
    clubs = data['Club']
    titles = data['Titres_Totales']

    # Create bar chart
    fig, ax = plt.subplots(figsize=(18, 6))
    ax.bar(clubs, titles)
    ax.set_xlabel('Les clubs de football', fontsize=15)
    ax.set_ylabel('Le nombre de titres de champions de France', fontsize=15)
    ax.set_title('Comparaison du nombres de titres de champions de France de football par club', fontsize=20)
    for i, v in enumerate(titles):
        ax.text(i, v + 0.1, str(v), color='black', fontweight='bold', fontsize=10, ha='center')
    plt.xticks(rotation=70, fontsize=10)

    # Save the visualization
    fig.savefig(path, bbox_inches='tight')
