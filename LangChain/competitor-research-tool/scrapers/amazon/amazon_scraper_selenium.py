import json
import re
import logging
import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from utils.selenium_driver import get_selenium_driver
from utils.url_utils import get_search_url

# Set up logging
log_file_path = os.path.join(os.path.dirname(__file__), 'amazon_scraper.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

def clear_log_file():
    """Clear the log file before writing new logs."""
    with open(log_file_path, 'w'):
        pass

def search_amazon_selenium(query="baseball", store="Amazon"):
    # Clear previous logs
    clear_log_file()

    driver = get_selenium_driver()
    if driver is None:
        logging.error("Failed to initialize Selenium WebDriver.")
        return {"error": "Failed to initialize Selenium WebDriver."}

    try:
        # Navigate to the search page
        search_url = get_search_url(store, query)
        print(f"Navigating to URL: {search_url}")
        driver.get(search_url)

        # Wait for the results container to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.s-main-slot')))
        print("Results container loaded")

        # Extract the page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        print("Page fetched and parsed with BeautifulSoup")

        # Extract totalResultCount from the script tag
        script_tag = soup.find("script", text=re.compile(r"P\.declare\('s\\-metadata'"))
        total_result_count = 0
        if script_tag:
            script_content = script_tag.string
            match = re.search(r'"totalResultCount":(\d+)', script_content)
            if match:
                total_result_count = int(match.group(1))
        print(f"Total result count: {total_result_count}")

        formatted_response = {"facets": [], "total_count": total_result_count, "facets_skipped": []}

        # Extract facet information without relying on specific DOM node types
        filters_section = soup.find(attrs={"data-component-type": "s-filters-panel-view"})
        if filters_section:
            facet_groups = filters_section.find_all(attrs={"role": "group"})
            for group in facet_groups:
                heading = group.find(attrs={"role": "heading"})
                if heading:
                    facet_name = heading.get_text(strip=True)
                    facet_values = []
                    unique_facet_values = set()
                    ul = group.find("ul")
                    if ul:
                        for li in ul.find_all("li"):
                            a_tag = li.find("a")
                            if a_tag:
                                facet_value = a_tag.get_text(strip=True)
                                if facet_value not in unique_facet_values:
                                    unique_facet_values.add(facet_value)
                                    print("Facet value:", facet_value)
                                    image_div = li.find("div", class_="colorsprite aok-float-left")
                                    if image_div:
                                        hovered_element = li.find("a", class_="a-link-normal s-navigation-item")
                                        title = hovered_element.get("title")
                                        facet_values.append(title)
                                    else:
                                        facet_values.append(facet_value)
                            print(f"Facet name: {facet_name}, value: {facet_value}")
                    if len(facet_values) == 0:
                        formatted_response["facets_skipped"].append(facet_name)
                    formatted_response["facets"].append({
                        "attrName": facet_name,
                        "values": facet_values
                    })
                    print(f"Facet name: {facet_name}, values: {facet_values}")

        print(f"Formatted response: {formatted_response}")
        return formatted_response
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()
        print("WebDriver quit")

def main():
    data = search_amazon_selenium("baseball", "Amazon")
    with open("amazon_facets.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Formatted response saved to amazon_facets.json")

if __name__ == "__main__":
    main()