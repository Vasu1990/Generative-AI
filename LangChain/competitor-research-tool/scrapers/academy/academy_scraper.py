import requests
import json

def search_academy(search_term="baseball", page_number=0, page_size=10):
    """
    Search Academy Sports + Outdoors products using their Search API
    """
    # URL
    url = f"https://www.academy.com/api/search/sitesearch/v2?searchTerm={search_term}&web=true&displayFacets=true&recordsPerPage=23&plpTilesPerPage=10&orderBy=mostRelevant&enableInventoryFacetCheck=true&b=null"

    # Headers
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1, i",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def main():
    # Example usage
    results = search_academy(search_term="baseball")
    if results:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main() 