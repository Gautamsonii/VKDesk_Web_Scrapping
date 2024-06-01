import requests
import json
import logging
from database import db  # Importing the database module

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(message)s')

# Define the MongoDB collection
collection = db.ajax_data

def save_to_mongo(data):
    try:
        if data:
            for item in data:
                # Check if the document already exists
                existing_count = collection.count_documents({
                    'title': item['title'],
                    'year': item['year']
                })
                if existing_count == 0:
                    collection.insert_one(item)
                    print(f"Inserted: {item['title']} - {item['year']}")
                else:
                    print(f"Already exists: {item['title']} - {item['year']}")
    except Exception as e:
        logging.error(f"Error saving AJax data to MongoDB: {e}")


def fetch_film_data(year):
    # Define the URL for the given year
    url = f'https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year={year}'

    # Send a GET request to the URL
    res = requests.get(url)

    # Check if the request was successful
    if res.status_code == 200:
        # Load the JSON response
        data = json.loads(res.content)

        # Check if data was found
        if data:
            # Print the year as the heading
            print(f"\nYear: {year}\n")

            # Prepare the data for MongoDB
            mongo_data = []
            for film in data:
                title = film.get('title', 'N/A')
                nominations = film.get('nominations', 'N/A')
                awards = film.get('awards', 'N/A')
                best_picture = 'Yes' if film.get('best_picture', False) else 'No'

                # Print the film data
                print(f"Title: {title}, Nominations: {nominations}, Awards: {awards}, Best Picture: {best_picture}")

                # Prepare the film data dictionary
                film_data = {
                    "year": year,
                    "title": title,
                    "nominations": nominations,
                    "awards": awards,
                    "best_picture": best_picture
                }
                mongo_data.append(film_data)

            # Save the data to MongoDB
            save_to_mongo(mongo_data)
        else:
            print(f"No data found for the year {year}.")
    else:
        print(f"Failed to fetch data for the year {year}. Status code: {res.status_code}")

for year in range(2010, 2016):
    fetch_film_data(year)
