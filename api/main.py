from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI(title="PatentMine API")

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "patents.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def serve_dashboard():
    dashboard_path = os.path.join(os.path.dirname(__file__), "..", "patentmine_dashboard.html")
    return FileResponse(dashboard_path)

@app.get("/patents")
def search_patents(q: str = "", mode: str = ""):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM patents WHERE 1=1"
    params = []
    
    if q:
        words = q.strip().split()
        word_conditions = []
        for w in words:
            if mode == 'competitor':
                word_conditions.append("(assignee LIKE ?)")
                params.extend([f"%{w}%"])
            elif mode == 'technology':
                word_conditions.append("(tech_domain LIKE ? OR abstract LIKE ? OR title LIKE ?)")
                params.extend([f"%{w}%", f"%{w}%", f"%{w}%"])
            else:
                word_conditions.append("(title LIKE ? OR abstract LIKE ? OR assignee LIKE ?)")
                params.extend([f"%{w}%", f"%{w}%", f"%{w}%"])
        query += " AND (" + " AND ".join(word_conditions) + ")"
        
    query += " ORDER BY utility_score DESC LIMIT 50"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM patents")
    total_found = cursor.fetchone()[0]
    conn.close()
    
    out = []
    for r in rows:
        d = dict(r)
        d['tags'] = ['lapsed']
        if d.get('utility_recency', 0) >= 80: d['tags'].append('new lapse')
        if d.get('utility_score', 0) >= 80: d['tags'].append('FTO clear')
        
        out.append({
            "id": d["id"],
            "title": d["title"],
            "assignee": d["assignee"],
            "lapse": d["lapse_date"],
            "citations": d["citation_count"] or 0,
            "score": round(d.get("utility_score", 0)),
            "recency": round(d.get("utility_recency", 0)),
            "prestige": round(d.get("utility_prestige", 0)),
            "breadth": round(d.get("utility_breadth", 0)),
            "tags": d['tags'],
            "tech": d["tech_domain"],
            "abstract": d["abstract"],
            "startup_pitch": d.get("startup_opportunity", ""),
            "country": d.get("country", "US / Global")
        })
        
    return {"patents": out, "total_found": total_found}

@app.get("/stats")
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patents")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT tech_domain, COUNT(*) as cnt FROM patents WHERE tech_domain IS NOT NULL GROUP BY tech_domain ORDER BY cnt DESC")
    domains = {row[0]: row[1] for row in cursor.fetchall() if row[0]}
    conn.close()
    return {"total_patents": total, "domains": domains}

class AlertRequest(BaseModel):
    patent_id: str
    email: str

@app.post("/watchlist")
def add_watchlist(req: AlertRequest):
    return {"message": "Success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
