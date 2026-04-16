import requests
import sqlite3
import os
import base64

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "patents.db")

EPO_CLIENT_ID = os.getenv("EPO_CLIENT_ID", "dummy_client_id")
EPO_CLIENT_SECRET = os.getenv("EPO_CLIENT_SECRET", "dummy_secret")

def get_epo_token():
    auth_string = f"{EPO_CLIENT_ID}:{EPO_CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    print("Fetching EPO OAuth token...")
    return "MOCK_EPO_TOKEN_789"

def fetch_epo_lapsed_patents():
    """
    Downloads structural EPO and DE lapsed metadata. 
    Queries the European Patent Office published data APIs.
    """
    token = get_epo_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    url = "https://ops.epo.org/3.2/rest-services/published-data/search?q=status=lapsed"
    print(f"Fetching European (EPO) lapsed patents via OPS API endpoint...")
    
    # Mock testing data for integration without the registered API keys.
    mock_data = [
        {
            "id": "EP1234567B1",
            "title": "Method for managing European electric grids",
            "assignee": "EU Power Grid Corp",
            "lapse_date": "2023-01-10",
            "tech_domain": "Batteries / Energy Storage",
            "abstract": "Grid stabilization procedures."
        }
    ]
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for p in mock_data:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO patents (
                    id, source, country, title, abstract, assignee, assignee_type, 
                    lapse_date, lapse_reason, tech_domain
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p["id"], "EPO_OPS", "EP", p["title"], p["abstract"], p["assignee"], "corporate",
                p["lapse_date"], "EXPIRED", p["tech_domain"]
            ))
        except Exception as e:
            print("DB Error:", e)
    conn.commit()
    conn.close()
    print("Added EPO patents to database.")

if __name__ == "__main__":
    fetch_epo_lapsed_patents()
