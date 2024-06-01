# VKDesk_Web_Scrapping

# Data Scraper

This repository contains a set of Python scripts to scrape data from the websites and store it in a MongoDB database.

## Files

1. `scraper.py`: Script to scrape film data for a range of years.
2. `database.py`: Module containing the MongoDB database connection.
3. `ajax.py`: Script to fetch AJAX film data and store it in the database.
4. `advanced.py`: Script to fetch normal data from front-end of website
5.  'main.py':  
6. 'config.py': Configuration file for MongoDB URI.

## Usage

1. Ensure you have Python installed on your system.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Modify the MongoDB connection details in `database.py` if necessary.
4. Run `scraper.py` to start scraping film data for the specified range of years.
5. The scraped data will be stored in the MongoDB database.

## Important Note

Make sure to handle sensitive information such as database credentials securely. Avoid hardcoding credentials directly into your scripts.

