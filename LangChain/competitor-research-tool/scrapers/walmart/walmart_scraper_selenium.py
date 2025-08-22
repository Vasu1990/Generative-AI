import json
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from utils.selenium_driver import get_selenium_driver
from utils.url_utils import get_search_url

def search_walmart_selenium(query, store):
    driver = get_selenium_driver()

    try:
        # Navigate to the search page
        search_url = get_search_url(store, query)
        print(f"Navigating to URL: {search_url}")
        driver.get(search_url)

        # Wait for the results container to load
        wait = WebDriverWait(driver, 10)
        results_container = wait.until(EC.presence_of_element_located((By.ID, 'results-container')))
        print("Results container loaded")

        # Extract the total count
        total_count = extract_total_count(results_container)
        print(f"Total count: {total_count}")

        formatted_response = {"facets": [], "total_count": total_count, "facets_skipped": []}

        # Extract filters sections
        filters_sections = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.expand-collapse-section')))
        print("Filters sections loaded")

        for filters_section in filters_sections:
            try:
                # Expand the filter group if collapsed
                expand_button = filters_section.find_element(By.CSS_SELECTOR, 'button[aria-expanded="false"]')
                driver.execute_script("arguments[0].click();", expand_button)
                print(f"Expanded filter group: {filters_section.get_attribute('outerHTML')}")
            except NoSuchElementException as e:
                print(f"Failed to expand filter group: {filters_section.get_attribute('outerHTML')}, Error: {e}")
                continue

            # Click "Show More" if it exists
            try:
                show_more_button = filters_section.find_element(By.XPATH, '//button[text()="Show More"]')
                if show_more_button:
                    driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
                    time.sleep(3)  # Allow time for scrolling
                    driver.execute_script("arguments[0].click();", show_more_button)
                    print("Clicked 'Show More' button")
                    time.sleep(1)
            except NoSuchElementException:
                print("No 'Show More' button found")
            except Exception as e:
                print(f"Failed to click 'Show More' button: {e}")

            # Extract the facet name
            facet_name = extract_facet_name(filters_section)
            print(f"Facet name: {facet_name}")
            facet_values = extract_facet_values(filters_section, facet_name, formatted_response)
            print(f"Facet values: {facet_values}")

            # Ensure facets are added even if count is None
            formatted_response["facets"].append({
                "attrName": facet_name,
                "values": facet_values
            })
        print(f"Formatted response: {json.dumps(formatted_response, indent=4)}")
        return formatted_response

    except Exception as e:
        print(f"Error: {e}")
        # print(f"Page HTML: {driver.page_source}")
        return None

    finally:
        driver.quit()
        print("WebDriver quit")

def extract_total_count(container):
    """Extracts the total count from the results container."""
    try:
        total_count_element = container.find_element(By.CSS_SELECTOR, '#results-container h2 span')
        total_count_text = total_count_element.text.strip('()')
        if '+' in total_count_text:
            return int(total_count_text.replace('+', '').replace(',', ''))
        return int(total_count_text.replace(',', ''))
    except Exception as e:
        print(f"Error extracting total count: {e}")
        return 0

def extract_facet_name(section):
    """Extracts the facet name from a filter section."""
    try:
        facet_element = section.find_element(By.CSS_SELECTOR, 'div.dib.pv3')
        return facet_element.text.strip()
    except Exception as e:
        print(f"Error extracting facet name: {e}")
        return ""

def extract_facet_values(section, facet_name, formatted_response):
    """Extracts the facet values from a filter section."""
    facet_values = []
    try:
        group_elements = section.find_elements(By.CSS_SELECTOR, '[role="group"], [role="radiogroup"]')
        for group_element in group_elements:
            if group_element.get_attribute('role') == 'group':
                value_elements = group_element.find_elements(By.CSS_SELECTOR, 'div.flex.justify-between.w-100')
                for value_element in value_elements:
                    try:
                        name = value_element.find_element(By.CSS_SELECTOR, 'input').get_attribute('value').strip()
                        count_element = value_element.find_element(By.CSS_SELECTOR, '.f6.nearer-mid-gray')
                        count = int(count_element.text.strip()) if count_element.text.strip().isdigit() else 0
                        facet_values.append({"name": name, "count": count})
                    except NoSuchElementException as e:
                        formatted_response["facets_skipped"].append(facet_name)
                        print(f"Error extracting facet value: {value_element.get_attribute('outerHTML')}, Error: {e}")
                        facet_values.append({"name": name, "count": 0})
            elif group_element.get_attribute('role') == 'radiogroup':
                if 'ml4' in group_element.get_attribute('class'):
                    value_elements = group_element.find_elements(By.CSS_SELECTOR, 'div.flex.justify-between')
                    for value_element in value_elements:
                        try:
                            label_element = value_element.find_element(By.CSS_SELECTOR, 'label')
                            name = label_element.find_element(By.CSS_SELECTOR, 'input').get_attribute('value').strip()
                            count_element = value_element.find_element(By.CSS_SELECTOR, '.f6.nearer-mid-gray')
                            count = int(count_element.text.strip()) if count_element.text.strip().isdigit() else 0
                            facet_values.append({"name": name, "count": count})
                        except NoSuchElementException as e:
                            formatted_response["facets_skipped"].append(facet_name)
                            print(f"Error extracting facet value: {value_element.get_attribute('outerHTML')}, Error: {e}")
                            facet_values.append({"name": name, "count": 0})
                else:
                    try:
                        name = group_element.find_element(By.CSS_SELECTOR, 'input').get_attribute('name').strip()
                        count_element = group_element.find_element(By.CSS_SELECTOR, '.f6.nearer-mid-gray')
                        count = int(count_element.text.strip()) if count_element.text.strip().isdigit() else 0
                        facet_values.append({"name": name, "count": count})
                    except NoSuchElementException as e:
                        formatted_response["facets_skipped"].append(facet_name)
                        print(f"Error extracting facet value: {group_element.get_attribute('outerHTML')}, Error: {e}")
                        facet_values.append({"name": name, "count": 0})
    except Exception as e:
        formatted_response.append(facet_name)
        print(f"Error extracting facet values: {e}")
    return facet_values

if __name__ == "__main__":
    data = search_walmart_selenium("baseball bats", "Walmart")
    with open("walmart_facets.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Formatted response saved to walmart_facets.json")