import pandas as pd
import sqlite3
import os
import io

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "patents.db")

def scrape_wipo_pct():
    """
    Simulates parsing the manual WIPO PATENTSCOPE CSV records tracking global PCT apps.
    """
    print("Processing WIPO PATENTSCOPE downloaded CSV records...")
    
    # Data mockup referencing the exact "CSV Download up to 10k" flow defined
    csv_mock = """PCT_ID,Title,Applicant,Status,PubDate
PCT/IB2010/12345,Global 5G Wireless Handover,Telecom Corp,ABANDONED,2010-09-01
PCT/US2015/99999,Pharmaceutical Composition,BioMed Lab,EXPIRED,2015-12-15
"""
    try:
        df = pd.read_csv(io.StringIO(csv_mock))
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        for idx, row in df.iterrows():
            pid = row["PCT_ID"]
            cursor.execute("""
                INSERT OR IGNORE INTO patents (
                    id, source, country, title, assignee, assignee_type, 
                    grant_date, lapse_reason, tech_domain
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pid, "WIPO_PCT", "WO", row["Title"], row["Applicant"], "corporate",
                row["PubDate"], row["Status"], "Digital Communications" 
            ))
            
        conn.commit()
        conn.close()
        print("Success! Inserted WIPO PCT applications into database.")
    except Exception as e:
        print("WIPO parse error:", e)

if __name__ == "__main__":
    scrape_wipo_pct()
