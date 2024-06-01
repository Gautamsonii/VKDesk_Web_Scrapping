import requests
import logging
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from database import db  # Importing the database module

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(message)s')

def save_to_mongo(data):
    try:
        if data:
            for item in data:
                # Check if the document already exists
                existing_count = db.forms_data.count_documents({
                    'team_name': item['team_name'],
                    'year': item['year']
                })
                if existing_count == 0:
                    db.forms_data.insert_one(item)
                    print(f"Inserted: {item['team_name']} - {item['year']}")
                else:
                    print(f"Already exists: {item['team_name']} - {item['year']}")
    except Exception as e:
        logging.error(f"Error saving forms data to MongoDB: {e}")

def scrape_url(url):
    try:
        session = requests.Session()
        retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        response = session.get(url)
        response.raise_for_status()
        
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

def parse_forms_data(html):
    data = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all('td')
            team = {
                'team_name': cols[0].text.strip(),
                'year': int(cols[1].text.strip()),
                'wins': int(cols[2].text.strip()),
                'losses': int(cols[3].text.strip()),
                'ot_losses': int(cols[4].text.strip()) if cols[4].text.strip() else None,
                'win_percentage': float(cols[5].text.strip()),
                'goals_for': int(cols[6].text.strip()),
                'goals_against': int(cols[7].text.strip()),
                'plus_minus': int(cols[8].text.strip())
            }
            data.append(team)
    except Exception as e:
        logging.error(f"Error parsing forms data: {e}")
    return data

def scrape_forms():
    base_url = "https://www.scrapethissite.com/pages/forms/?page_num="
    page_num = 1
    while True:
        url = base_url + str(page_num)
        html = scrape_url(url)
        if not html:
            break
        data = parse_forms_data(html)
        if not data:
            break
        save_to_mongo(data)
        page_num += 1

if __name__ == "__main__":
    scrape_forms()


import requests
import logging
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from database import db  # Importing the database module

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(message)s')

def save_to_mongo(data):
    try:
        if data:
            # Assuming each item in data has a 'team_name' and 'year' field
            for item in data:
                # Check if the document already exists
                existing_count = db.forms_data.count_documents({
                    'team_name': item['team_name'],
                    'year': item['year']
                })
                if existing_count == 0:
                    db.forms_data.insert_one(item)
                    print(f"Inserted: {item['team_name']} - {item['year']}")
                else:
                    print(f"Already exists: {item['team_name']} - {item['year']}")
    except Exception as e:
        logging.error(f"Error saving forms data to MongoDB: {e}")

def scrape_url(url):
    try:
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["GET", "POST"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        response = session.get(url)
        response.raise_for_status()
        
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

def parse_forms_data(html):
    data = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all('td')
            team = {
                'team_name': cols[0].text.strip(),
                'year': int(cols[1].text.strip()),
                'wins': int(cols[2].text.strip()),
                'losses': int(cols[3].text.strip()),
                'ot_losses': int(cols[4].text.strip()) if cols[4].text.strip() else None,
                'win_percentage': float(cols[5].text.strip()),
                'goals_for': int(cols[6].text.strip()),
                'goals_against': int(cols[7].text.strip()),
                'plus_minus': int(cols[8].text.strip())
            }
            data.append(team)
    except Exception as e:
        logging.error(f"Error parsing forms data: {e}")
    return data

def scrape_forms():
    base_url = "https://www.scrapethissite.com/pages/forms/?page_num="
    page_num = 1
    while True:
        url = base_url + str(page_num)
        html = scrape_url(url)
        if not html:
            break
        data = parse_forms_data(html)
        if not data:
            break
        save_to_mongo(data)
        page_num += 1

if __name__ == "__main__":
    scrape_forms()
