import time
import requests
import sqlite3
import os
import json
from bs4 import BeautifulSoup

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "patents.db")

def scrape_google_patent(patent_id: str):
    """
    Scrapes patents.google.com for abstract, full claims, cited-by count, and PDF link.
    Rate limit: 1 request / 2 seconds as per guidelines.
    """
    url = f"https://patents.google.com/patent/{patent_id}/en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    print(f"Scraping Google Patents for {patent_id}...")
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")

        # Extract abstract
        abstract_section = soup.find("section", itemprop="abstract")
        abstract = abstract_section.text.strip() if abstract_section else "N/A"

        # Extract claims
        claims_divs = soup.find_all("div", class_="claim-text")
        claims = [c.text.strip() for c in claims_divs]
        
        # Get cited-by count (Forward citations approximation)
        cited_by_count = 0 
        forward_ref_header = soup.find(lambda tag: tag.name == "h2" and "Cited By" in tag.text)
        if forward_ref_header:
            table = forward_ref_header.find_next("table")
            if table:
                cited_by_count = len(table.find_all("tr")) - 1

        # Get PDF link
        pdf_link = ""
        pdf_a = soup.find("a", {"itemprop": "pdfLink"})
        if pdf_a:
            pdf_link = pdf_a.get("href", "")

        data = {
            "id": patent_id,
            "abstract": abstract,
            "claims": claims,
            "citation_count": cited_by_count,
            "pdf_link": pdf_link
        }
        
        update_db(data)
        return data
        
    except Exception as e:
        print(f"Error scraping Google Patents for {patent_id}: {e}")
        return None
    finally:
        # Crucial rate limit: 1 request per 2 seconds
        time.sleep(2)

def update_db(data):
    """ Update the SQLite DB with the enriched Google Patents data """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE patents 
            SET abstract = ?, citation_count = ?
            WHERE id = ?
        """, (data["abstract"], data["citation_count"], data["id"]))
        conn.commit()
    except Exception as e:
        print(f"DB Update Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Test execution
    res = scrape_google_patent("US7234567B2")
    print(json.dumps(res, indent=2))
