# utils/url_utils.py
import urllib.parse

def get_search_url(store, query):
    encoded_query = urllib.parse.quote(query)
    if store == "Lowe's":
        return f"https://www.lowes.com/search?searchTerm={encoded_query}"
    elif store == "Walmart":
        return f"https://www.walmart.com/search/?query={encoded_query}"
    elif store == "Amazon":
        return f"https://www.amazon.com/s?k={encoded_query}"
    elif store == "Home Depot":
        return f"https://www.homedepot.com/s/{encoded_query}"
    elif store == "Tractor Supply":
        return f"https://www.tractorsupply.com/tsc/search/{encoded_query}"
    elif store == "Dick's":
        return f"https://www.dickssportinggoods.com/search/SearchDisplay?searchTerm={encoded_query}"
    elif store == "Academy":
        return f"https://www.academy.com/search?searchTerm={encoded_query}"
    else:
        raise ValueError(f"Unknown store: {store}")