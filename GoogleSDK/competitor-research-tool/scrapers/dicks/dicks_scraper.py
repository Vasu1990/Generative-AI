import requests
import json

def search_dicks_sporting(search_term="baseball bats", page_number=0, page_size=48, store_id="1325", zip_code="77056", store="Dick's"):
    # Base URL
    url = "https://prod-catalog-product-api.dickssportinggoods.com/v2/search"
    
    # Search parameters
    search_params = {
        "pageNumber": page_number,
        "pageSize": page_size,
        "selectedSort": 0,
        "selectedStore": store_id,
        "storeId": "15108",
        "zipcode": zip_code,
        "isFamilyPage": False,
        "mlBypass": False,
        "snbAudience": "",
        "searchTerm": search_term
    }
    
    # Headers
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-GB;q=0.6,en-US;q=0.5",
        "channel": "dsg",
        "content-type": "application/json",
        "disable-pinning": "false",
        "origin": "https://www.dickssportinggoods.com",
        "pool-c-swimlane": "67",
        "priority": "u=1, i",
        "referer": "https://www.dickssportinggoods.com/search/SearchDisplay",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    # Convert search parameters to URL-encoded JSON string
    params = {"searchVO": json.dumps(search_params)}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def main():
    # Example usage
    results = search_dicks_sporting()
    if results:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()