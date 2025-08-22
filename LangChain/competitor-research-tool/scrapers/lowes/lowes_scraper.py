import requests
import json

def search_lowes(query="grills%20outdoor%20cooking"):
    url = "https://www.lowes.com/search/products"
    params = {
        "searchTerm": query,
        "ac": False,
        "algoRulesAppliedInPageLoad": False
    }
    
    # Headers
    headers = {
        "priority": "u=1, i",
        "referer": "https://www.lowes.com/search?searchTerm=grills&refinement=4294963688",
        "sec-ch-ua":'"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def main():
    # Example usage
    results = search_lowes()
    if results:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()