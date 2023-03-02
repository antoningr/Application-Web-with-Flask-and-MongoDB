
from flask import Flask, render_template
from pymongo import MongoClient


# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['football']
collection = db['ranking']


# Create search function
def search_clubs(query , match_played_only = False , goal_scored_only = False, position_only = False , tri_croissant = None , tri_decroissant = None):
    
    # Build the query
    query_dict = {"Club": {'$regex': f'.*{query}.*', '$options': 'i'}}  
    
    # Update the documents to convert the "Match_Joue" column to integers
    docs = collection.find({})
    for doc in docs:
        match_joue = int(doc['Match_Joue'])
        collection.update_one({'_id': doc['_id']}, {'$set': {'Match_Joue': match_joue}})
        
    # Update the documents to convert the "But_Pour" column to integers
    docs = collection.find({})
    for doc in docs:
        but_pour = int(doc['But_Pour'])
        collection.update_one({'_id': doc['_id']}, {'$set': {'But_Pour': but_pour}})
    
    # Update the documents to convert the "But_Contre" column to integers
    docs = collection.find({})
    for doc in docs:
        position = int(doc['Position'])
        collection.update_one({'_id': doc['_id']}, {'$set': {'Position': position}}) 


    # Update the documents to convert the "But_Contre" column to integers
    if match_played_only:
        
        projection = {"_id": 0, "Club": 1, "Match_Joue": 1}
        cursor = collection.find(query_dict, projection)
        results = []
        
        for result in cursor:
            Club = result["Club"]
            Match_Joue = result.get("Match_Joue", 0)
            results.append({"Club": Club, "Match_Joue": Match_Joue})

        if tri_croissant:
            results.sort(key=lambda x: x["Match_Joue"])
        elif tri_decroissant:
            results.sort(key=lambda x: x["Match_Joue"], reverse=True)
        
        if results is not None:
            results = [f"{result['Club']} a joué {result.get('Match_Joue', 0)} matchs" for result in results]
            results = "\n".join(results)
        else:
            results = "Aucun résultat trouvé."
        return results
    
    # Update the documents to convert the "But_Contre" column to integers
    if goal_scored_only :
        
        projection = {"_id": 0, "Club": 1, "But_Pour": 1}
        cursor = collection.find(query_dict, projection)
        results = []
        
        for result in cursor:
            Club = result["Club"]
            But_Pour = result.get("But_Pour", 0)
            results.append({"Club": Club, "But_Pour": But_Pour})
    
        if tri_croissant:
            results.sort(key=lambda x: x["But_Pour"])
        elif tri_decroissant:
            results.sort(key=lambda x: x["But_Pour"], reverse=True)

        if results is not None:
            results = [f"{result['Club']} a marqué {result.get('But_Pour', 0)} buts" for result in results]
            results = "\n".join(results)
        else:
            results = "Aucun résultat trouvé."
        return results
    
    # If the user wants to search by position
    if position_only :
            
            projection = {"_id": 0, "Club": 1, "Position": 1}
            cursor = collection.find(query_dict, projection)
            results = []
            
            for result in cursor:
                Club = result["Club"]
                Position = result.get("Position", 0)
                results.append({"Club": Club, "Position": Position})
    
            if tri_croissant:
                results.sort(key=lambda x: x["Position"])
            elif tri_decroissant:
                results.sort(key=lambda x: x["Position"], reverse=True)
            if results is not None:
                results = [f"{result['Club']} est classé {result.get('Position', 0)}" for result in results]
                results = "\n".join(results)
            else:
                results = "Aucun résultat trouvé."
              
            return results

    # If the user wants to search by position
    if match_played_only == False and goal_scored_only == False and position_only == False:
        
        # Get the list of unique clubs
        clubs_uniques = collection.distinct("Club", query_dict)
        
        if len(clubs_uniques) == 0:
            results="Aucun club ne correspond à votre recherche."
        
        else:
            results = ""
        
            # Get the information of each club
            for club in clubs_uniques:
                
                # Get the information of the club
                club_infos = []
                club_infos = collection.find_one({"Club": {'$eq': club}})

                if club_infos is not None:
                    
                    # Get the club name
                    results += club_infos['Club'] + "\n"
                    
                    # Get the other information
                    for key, value in club_infos.items():
                        if key != "Club" and key != "_id":
                            results += f"{key.replace('_' ,' ')} : {str(value)}\n"
                    results += "\n\n"
            
    return results
