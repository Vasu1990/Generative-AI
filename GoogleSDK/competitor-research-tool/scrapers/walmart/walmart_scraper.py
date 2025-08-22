import requests
import json

def search_walmart(query="grills"):
    # Base URL
    url = "https://www.walmart.com/orchestra/snb/graphql/Search/10bdb143060c80489541895e9d22552850d93d8e49702abfcab2d11640a1bd51/search"


    inputJson = { "id": "", "dealsId": "", "query": query, "page": 1, "prg": "desktop", "catId": "", "facet": "", "sort": "best_match", "rawFacet": "", "seoPath": "", "ps": 40, "limit": 40, "ptss": "", "trsp": "", "beShelfId": "", "recall_set": "", "module_search": "", "min_price": "", "max_price": "", "storeSlotBooked": "", "additionalQueryParams": { "hidden_facet": None, "translation": None, "isMoreOptionsTileEnabled": True, "isGenAiEnabled": True }, "searchArgs": { "query": "grills", "cat_id": "", "prg": "desktop", "facet": "" }, "ffAwareSearchOptOut": False, "fitmentFieldParams": { "powerSportEnabled": True, "dynamicFitmentEnabled": True, "extendedAttributesEnabled": True }, "fitmentSearchParams": { "id": "", "dealsId": "", "query": query, "page": 1, "prg": "desktop", "catId": "", "facet": "", "sort": "best_match", "rawFacet": "", "seoPath": "", "ps": 40, "limit": 40, "ptss": "", "trsp": "", "beShelfId": "", "recall_set": "", "module_search": "", "min_price": "", "max_price": "", "storeSlotBooked": "", "additionalQueryParams": { "hidden_facet": None, "translation": None, "isMoreOptionsTileEnabled": True, "isGenAiEnabled": True }, "searchArgs": { "query": "grills", "cat_id": "", "prg": "desktop", "facet": "" }, "ffAwareSearchOptOut": False, "cat_id": "", "_be_shelf_id": "" }, "enableFashionTopNav": False, "enableRelatedSearches": True, "enablePortableFacets": True, "enableFacetCount": True, "fetchMarquee": True, "fetchSkyline": True, "fetchGallery": False, "fetchSbaTop": True, "enableAdsPromoData": False, "fetchDac": False, "tenant": "WM_GLASS", "enableMultiSave": False, "enableInStoreShelfMessage": False, "enableSellerType": False, "enableAdditionalSearchDepartmentAnalytics": False, "enableFulfillmentTagsEnhacements": False, "enableRxDrugScheduleModal": False, "enablePromoData": False, "enableSignInToSeePrice": False, "enablePromotionMessages": False, "enableItemLimits": False, "enableCanAddToList": False, "enableIsFreeWarranty": False, "enableShopSimilarBottomSheet": False, "pageType": "SearchPage" }

    params = {
        "variables": json.dumps(inputJson)
    }
    # Headers
    headers = {
        "device_profile_ref_id": "oyz2h9bqsagguvwdeczvyuphmok1kfxm4dqt",
        "downlink": "10",
        "dpr": "1.25",
        "priority": "u=1, i",
        "referer": "https//www.walmart.com/search?q=grills",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "tenant-id": "elh9ie",
        "traceparent": "00-18237b656e8da35bf44279e2135f281f-a6eb1d65c3140769-00",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "wm_mp": "true",
        "wm_page_url": "https://www.walmart.com/search?q=" + query,
        "wm_qos.correlation_id": "T10NbEsOtQrcmpbE7Ztq-u4U7OQ_9xacFG-m",
        "x-apollo-operation-name": "Search",
        "x-enable-server-timing": "1",
        "x-latency-trace": "1",
        "x-o-bu": "WALMART-US",
        "x-o-ccm": "server",
        "x-o-correlation-id": "T10NbEsOtQrcmpbE7Ztq-u4U7OQ_9xacFG-m",
        "x-o-gql-query": "query Search",
        "x-o-mart": "B2C",
        "x-o-platform": "rweb",
        "x-o-platform-version": "us-web-1.178.0-b824b35436eb64e9e9fd713d8eb1ce2f33c74bee-020623",
        "x-o-segment": "oaoh",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US",
        "baggage": "trafficType=customer,deviceType=desktop,renderScope=CSR,webRequestSource=Browser,pageName=searchResults,isomorphicSessionId=RyqCqZjcklUmEuhtH0AmB,renderViewId=618dc15d-5c73-4a32-8817-8ebd54a57667",
        "content-type": "application/json"
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
    results = search_walmart()
    if results:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()