import requests
import json
import time

def cross_reference_openalex(inventor_name: str, institution: str = None):
    """
    Looks up an inventor/institution in OpenAlex to find their published papers.
    Matches patent inventors to their papers. Builds the "research-to-market gap" feature.
    """
    print(f"Querying OpenAlex API for {inventor_name}...")
    base_url = "https://api.openalex.org/works"
    
    # We query for works matching the author name
    params = {
        "search": inventor_name,
        "per-page": 5, # Just grab the top 5 related works
    }
    
    if institution:
        params["search"] += f" {institution}"
        
    try:
        res = requests.get(base_url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        
        matches = []
        for work in data.get("results", []):
            matches.append({
                "title": work.get("title"),
                "doi": work.get("doi"),
                "citations": work.get("cited_by_count", 0),
                "publication_year": work.get("publication_year")
            })
            
        return matches
    except Exception as e:
        print(f"Error querying OpenAlex API: {e}")
        return []
    finally:
        time.sleep(1)

if __name__ == "__main__":
    # Test execution
    res = cross_reference_openalex("Geoffrey Hinton", "Toronto")
    print(json.dumps(res, indent=2))
