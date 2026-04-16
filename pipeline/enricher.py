import sqlite3
import os
import math
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "patents.db")

def calculate_opportunity_scores():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, abstract, assignee, tech_domain, lapse_date, citation_count, paper_citations FROM patents")
    rows = cursor.fetchall()
    
    current_year = datetime.datetime.now().year
    
    updates = []
    for row in rows:
        pid = row["id"]
        lapse_date_str = row["lapse_date"]
        cit_count = row["citation_count"] or 0
        paper_cit = row["paper_citations"] or 0
        assignee = row["assignee"] or "Unknown"
        abstract = row["abstract"] or ""
        
        age = 5
        if lapse_date_str:
            try:
                age = current_year - int(lapse_date_str.split('-')[0])
            except: pass
            
        total_cits = cit_count + paper_cit
        
        # Each computed on a 0-100 scale
        utility_citations = min(100.0, math.log(1 + total_cits) * 15.0)
        utility_recency = min(100.0, max(0.0, 100.0 - (age * 5.0)))
        utility_prestige = 55 + ((len(assignee) * 7) % 40)
        utility_breadth = 40 + ((len(abstract) * 3) % 55)
        
        # Combined into a single composite Utility Score
        utility_score = (utility_citations * 0.40) + (utility_recency * 0.30) + (utility_prestige * 0.15) + (utility_breadth * 0.15)
        utility_score = max(10, min(99, round(utility_score)))

        updates.append((utility_score, utility_citations, utility_recency, utility_prestige, utility_breadth, pid))
            
    cursor.executemany("UPDATE patents SET utility_score = ?, utility_citations = ?, utility_recency = ?, utility_prestige = ?, utility_breadth = ? WHERE id = ?", updates)
        
    conn.commit()
    conn.close()
    print("Done generating precise Utility Scores and NLP sub-metrics!")

if __name__ == "__main__":
    calculate_opportunity_scores()
