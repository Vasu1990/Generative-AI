import json
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from utils.selenium_driver import get_selenium_driver
from utils.url_utils import get_search_url

def search_home_depot_selenium(query, store):
    driver = get_selenium_driver()
    if driver is None:
        print("Failed to initialize Selenium WebDriver.")
        return {"error": "Failed to initialize Selenium WebDriver."}

    try:
        # Navigate to the search page
        search_url = get_search_url(store, query)
        print(f"Navigating to URL: {search_url}")
        driver.get(search_url)

        wait = WebDriverWait(driver, 10)

        # Extract the text "66 Results" using XPath
        results_text_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                    '.sui-self-end.results-applied__primary-filter-label.results-applied__primary-filter-label-GIF-plp')))
        results_text = results_text_element.text
        # Extract only the number from the text
        results_number = results_text.split(' ')[0]
        print(f"Results number: {results_number}")

        formatted_response = {"facets": [], "total_count": results_number, "facets_skipped": []}

        # Scroll down to the "All Filters" button and click it
        all_filters_button = driver.find_element(By.CSS_SELECTOR, '.view-all-button')
        driver.execute_script("arguments[0].scrollIntoView();", all_filters_button)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", all_filters_button)
        print("Clicked 'All Filters' button")
        time.sleep(1)

        # Wait for the filters to load
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.dimensions')))
        print("Filters loaded")

        # Extract filter sections
        filter_sections = driver.find_elements(By.CSS_SELECTOR, '.dimension.dimension--drawer.dimension--padding')
        print(f"Filter sections loaded: {len(filter_sections)}")

        for section in filter_sections:
            try:
                facet_values = []
                facet_button = section.find_element(By.CSS_SELECTOR, '.dimension__label')
                driver.execute_script("arguments[0].scrollIntoView();", facet_button)
                time.sleep(2)
                facet_name = facet_button.text
                print(f"Facet name: {facet_name}")
                time.sleep(2)
                driver.execute_script("arguments[0].click();", facet_button)
                time.sleep(2)
                values = section.find_elements(By.CSS_SELECTOR, '.refinement__link')
                print(f"Values: {len(values)}")
                if len(values) > 0:
                    for value in values:
                        try:
                            facet_values.append({"name": value.text, "count": 'NA'})
                        except NoSuchElementException as e:
                            print(f"Error extracting facet value: {e}")
                            formatted_response["facets_skipped"].append(facet_name)
                        except Exception as e:
                            print(f"Error: {e}")
                            formatted_response["facets_skipped"].append(facet_name)
                else:
                    rating_elements = section.find_elements(By.CSS_SELECTOR, '.rating-start__label')
                    for rating_element in rating_elements:
                        rating_text = rating_element.text
                        print(f"Rating text: {rating_text}")
                        facet_values.append({"name": rating_text, "count": 'NA'})
                    if len(facet_values)==0:
                        print(f"Skipping facet: {facet_name}")
                        formatted_response["facets_skipped"].append(facet_name)
                formatted_response["facets"].append({
                    "attrName": facet_name,
                    "values": facet_values
                })
            except NoSuchElementException as e:
                print(f"Error extracting facet value: {e}")
                formatted_response["facets_skipped"].append(facet_name)
            except Exception as e:
                print(f"Error: {e}")
                formatted_response["facets_skipped"].append(facet_name)
        print(f"Formatted response: {formatted_response}")
        return formatted_response
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()
        print("WebDriver quit")

if __name__ == "__main__":
    data = search_home_depot_selenium("drill", "Home Depot")
    with open("home_depot_facets.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Formatted response saved to home_depot_facets.json")