import requests
import json

def search_tractor_supply(query="grills%20outdoor%20cooking"):
    url = "https://www.tractorsupply.com/gtwy/SiteSearch/catalogSearch"
    params = {
        "searchType": "keyword",
        "minAttr": "true",
        "storeNumber": 2314,
        "pageNumber": 1,
        "pageSize": 50,
        "q": query,
        "categoryId": "",
        "sort": 0,
        "i": "6f7cbf1b-db62-4fcf-bfa6-209ad2817c2f",
        "s": 1
    }
    
    # Headers
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Channel": "web",
        "Priority": "u=1, i",
        "Referer": "https://www.tractorsupply.com/tsc/search/grills%20outdoor%20cooking?isIntSrch=written",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "X-Api-Version": "v2",
        "X-Dtpc": "30$550744688_465h10vSHCQUPTPAPPUHCQRGKKIBSHMWKDKAMAV-0e0",
        "Zoneid": "53"
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
    results = search_tractor_supply()
    if results:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()