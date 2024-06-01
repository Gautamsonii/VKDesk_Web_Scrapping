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
            existing_count = db.advanced_data.count_documents({'header': data[0]['header']})
            if existing_count == 0:
                db.advanced_data.insert_many(data)
                print("Advanced data inserted successfully.")
            else:
                print("Advanced data already exists in the database.")
    except Exception as e:
        logging.error(f"Error saving advanced data to MongoDB: {e}")

def scrape_url(url):
    try:
        session = requests.Session()
        # retry_strategy = Retry(
        #     total=3,
        #     status_forcelist=[429, 500, 502, 503, 504],
        #     method_whitelist=["GET", "POST"],
        #     backoff_factor=1
        # )
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

def parse_advanced_data(html):
    data = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        header = soup.find('h3').text.strip()
        lead_paragraph = soup.find('p', class_='lead').text.strip()
        data.append({
            'header': header,
            'lead_paragraph': lead_paragraph,
            'topics': []
        })

        sections = soup.find_all('h4')
        for section in sections:
            topic = section.text.strip()
            description = section.find_next_sibling('p').text.strip()
            data[0]['topics'].append({
                'topic': topic,
                'description': description
            })
    except Exception as e:
        logging.error(f"Error parsing advanced data: {e}")
    return data

def scrape_advanced():
    url = "https://www.scrapethissite.com/pages/advanced/"
    html = scrape_url(url)
    if html:
        data = parse_advanced_data(html)
        save_to_mongo(data)

if __name__ == "__main__":
    scrape_advanced()
