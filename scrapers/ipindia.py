import sqlite3
import datetime
import requests
from bs4 import BeautifulSoup
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "patents.db")

# The URL for IP India Expired Patents register
# Often you need to figure out the exact endpoint, this is a placeholder URL
EXPIRED_REGISTER_URL = "https://iprsearch.ipindia.gov.in/PublicSearch/" 

def fetch_ceased_patents():
    """
    Scrape the IP India expired register (u/s 53(2)) to get a list of lapsed patent IDs.
    """
    print(f"Fetching expired register from {EXPIRED_REGISTER_URL}...")
    # NOTE: Scraping IP India might require setting headers or handling basic forms.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        response = requests.get(EXPIRED_REGISTER_URL, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        # TODO: Parse the actual table or div housing the "u/s 53(2)" lapsed patents list.
        # This is a mock extraction for now.
        lapsed_patents = []
        # Return a sample for structural testing
        return [
            {"id": "IN253123", "title": "Sample Indian Patent 1"},
            {"id": "IN345678", "title": "Sample Indian Patent 2"}
        ]
        
    except Exception as e:
        print(f"Error fetching IP India Expired Register: {e}")
        return []

def scrape_inpass_details(patent_id):
    """
    Scrape InPASS for detailed information on a specific Indian patent.
    Extracts: applicant, IPC class, grant date, status.
    """
    print(f"Fetching details for {patent_id} from InPASS...")
    # TODO: Implement InPASS detailed scraping
    # Placeholder details
    return {
        "abstract": "A placeholder abstract for " + patent_id,
        "assignee": "Example Indian Univ",
        "assignee_type": "university",
        "grant_date": "2015-01-01",
        "lapse_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "lapse_reason": "FEE_NOT_PAID",
        "ipc_codes": json.dumps(["A61K"]),
        "tech_domain": "Pharmaceuticals"
    }

def save_to_db(patent_data):
    """
    Save the extracted patent to the SQLite database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO patents (
                id, source, country, title, abstract, assignee, assignee_type, 
                grant_date, lapse_date, lapse_reason, ipc_codes, tech_domain, scraped_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patent_data["id"],
            "IPINDIA",
            "IN",
            patent_data.get("title", ""),
            patent_data.get("abstract", ""),
            patent_data.get("assignee", ""),
            patent_data.get("assignee_type", ""),
            patent_data.get("grant_date", ""),
            patent_data.get("lapse_date", ""),
            patent_data.get("lapse_reason", ""),
            patent_data.get("ipc_codes", "[]"),
            patent_data.get("tech_domain", ""),
            datetime.datetime.now().isoformat()
        ))
        conn.commit()
        print(f"Saved {patent_data['id']} to DB.")
    except Exception as e:
        print(f"Database error for {patent_data['id']}: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Test execution
    patents = fetch_ceased_patents()
    for p in patents:
        details = scrape_inpass_details(p["id"])
        details.update(p)
        save_to_db(details)
    print("Done IP India scrape.")
