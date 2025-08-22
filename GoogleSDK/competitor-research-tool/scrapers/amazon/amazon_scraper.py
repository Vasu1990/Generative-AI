import requests
from bs4 import BeautifulSoup
import json
import re

def search_amazon(query="baseball"):
    # Base URL
    url = f"https://www.amazon.com/s?k={query}"
    
    # Headers
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en,en-US;q=0.9,ak;q=0.8,ar;q=0.7",
        "cache-control": "no-cache",
        "cookie": "session-id=133-9756058-2193539; ubid-main=131-4209389-4979425; at-main=Atza|IwEBIFUCkcG4T9HxMREB1jMppLpSsWw7IwooHmrS5IGoLfaP10FDULJresrjDihPZtPMajZc7kh50bBbr3s6gC23EeMw4j_B1DU5OkmfwyKPJY1dVNsKeQ1LS7V8ofjGNcufPpALpwPWVFlwdcp2lwWKvQLm3PxWwnynD7CpCSKPYor__kXEIjHoNfB9bl_TUYejjeBdQkaPe6npMagqZrnR_37vQkC8bH2WTkAkLXXExwPqtg; sess-at-main=\"AtwLDAmdoi7Ducl1YpM7jLhFCagY6kwkJqi4Tfsaydk=\"; sst-main=Sst1|PQH_hojafO5nq-kfdyj8ar9qCVcbdf-smluNANshKgJDSOnSan8xrNx9H69ys47JinAoNkM4WQcldrni1lqSZ-LKEARPJXiUQkU7UMR1zXmgv6mD9d-Lfot0gSCQ2IySCkTv4GniKBuCRsEP8bMHczCyUjwtag591eGHQGMeBR_V5cDhYfK82aqCMnO9XVU4L_nTDr6qUVIWzhqUU5bOUv5P1EsK4dYQlVTObjNabC5NsOvIRu0Ljrk6wCzqbv-nwjPBu_YvOlg4yiZt4TqGIJRtEAAE4L97Sot4ocWXswrtUBk; session-id-time=2082787201l; i18n-prefs=USD; lc-main=en_US; skin=noskin; session-token=anE1Y+ZecfdyjN3T7as1yael2q65j5HwaxVd78IjfKVArIcy5lpSfWzht6QJ4Cpg/U1A8UyBd6O9PjlnMJitHFlWaOhaY9SOUoku3LnAKwCDGOvszzjU621rxhyFJcE5a1gX2TgGIOxQcZchkTj0+s5Ce4NQ/4zSHQatSgBj1Dq3PTTdSOIz9RUx2VZJLDTuH4uFHWfit8QXGMtkhADgEoE9Ke4qvAkOoROlCiKdlwBOlU9xE5FzZiFf8NlgDCElJe4gT40pTF+O/a/LvpVXf0oWKxxXADUSxU77KZu6NCQGpI3QawOwaAVjSZvI+6BYtENh2vQyhC7Kh1HAwkIfZTdF5jliHL2fPJjK24Pmza6Qje76ew0JGJCvrV48y+5r; x-main=MPgPtddQPsVJtrFpklQEkp6A1dmpH3OrtHUR19GUKhpfzkt5zWeU5BFyAbiZGDHW; csm-hit=tb:3W4MWC3XGCW9N57Y822Y+s-60MKXTD96ENP08SC9MZH|1739516191996&t:1739516191996&adb:adblk_no",
        "device-memory": "8",
        "downlink": "9.25",
        "dpr": "2",
        "ect": "4g",
        "mode": "stage",
        "pragma": "akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-extracted-values, akamai-x-get-nonces, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no",
        "priority": "u=0, i",
        "rtt": "50",
        "sec-ch-device-memory": "8",
        "sec-ch-dpr": "2",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-ch-viewport-width": "1792",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "viewport-width": "1792"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": f"Failed to fetch page, status code: {response.status_code}"}

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract totalResultCount from the script tag
        script_tag = soup.find("script", text=re.compile(r"P\.declare\('s\\-metadata'"))
        total_result_count = 0
        if script_tag:
            script_content = script_tag.string
            match = re.search(r'"totalResultCount":(\d+)', script_content)
            if match:
                total_result_count = int(match.group(1))

        formatted_response = {"facets": [], "total_count": total_result_count}

        # Extract facet information without relying on specific DOM node types
        filters_section = soup.find(attrs={"data-component-type": "s-filters-panel-view"})
        if filters_section:
            facet_groups = filters_section.find_all(attrs={"role": "group"})
            for group in facet_groups:
                heading = group.find(attrs={"role": "heading"})
                if heading:
                    facet_name = heading.get_text(strip=True)
                    facet_values = []
                    ul = group.find("ul")
                    if ul:
                        for li in ul.find_all("li"):
                            facet_values.append(li.get_text(strip=True))
                    formatted_response["facets"].append({
                        "attrName": facet_name,
                        "values": facet_values
                    })

        # Log the response
        print(json.dumps(formatted_response, indent=4))
        return formatted_response
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def main():
    data = search_amazon("baseball")
    with open("amazon_facets.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Formatted response saved to amazon_facets.json")

if __name__ == "__main__":
    main()