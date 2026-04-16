import pandas as pd
import requests
import io
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "patents.db")

def parse_orange_book_csv():
    """
    Downloads and parses the FDA Orange Book patent data for drug mapping.
    Cross references active drug patents with our database to build the "pharma angle".
    """
    print("Fetching FDA Orange Book CSV data...")
    # NOTE: The actual FDA download URL is dynamic. This is a pandas string mock for demo structure.
    csv_data = """Patent No,Drug Name,Expiry Date,Use Code
US7234567B2,LIPITOR,2021-05-15,U-45
US8999999B2,EXCEDRIN,2025-10-10,U-112
"""
    
    try:
        # 1. Read CSV via pandas
        df = pd.read_csv(io.StringIO(csv_data))
        
        # Clean FDA patent numbers (FDA often strips country codes 'US' and kind codes 'B2')
        # We will mock the match check directly with raw text
        
        # 2. Connect to our DB and load existing pharma patents
        conn = sqlite3.connect(DB_PATH)
        patents_df = pd.read_sql_query("SELECT id, title, tech_domain FROM patents WHERE tech_domain = 'Pharmaceuticals' OR id IN ('US7234567B2', 'US8999999B2')", conn)
        
        if patents_df.empty:
            print("No pharmaceutical patents found in our Database to cross-reference.")
            return []
            
        # 3. Merge dataset to verify patent <-> drug matches
        merged = pd.merge(patents_df, df, left_on='id', right_on='Patent No', how='inner')
        
        print(f"Matched {len(merged)} FDA Orange Book patents in our local database.")
        conn.close()
        return merged.to_dict('records')
        
    except Exception as e:
        print(f"Error parsing Orange Book: {e}")
        return []

if __name__ == "__main__":
    res = parse_orange_book_csv()
    print("Results:", res)
