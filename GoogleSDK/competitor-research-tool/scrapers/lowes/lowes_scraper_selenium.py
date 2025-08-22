import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from utils.selenium_driver import get_selenium_driver
from utils.url_utils import get_search_url

def safe_find_element(driver, by, value, retries=3):
    for i in range(retries):
        try:
            element = driver.find_element(by, value)
            return element
        except StaleElementReferenceException:
            if i < retries - 1:
                time.sleep(1)
            else:
                raise

def safe_find_elements(driver, by, value, retries=3):
    for i in range(retries):
        try:
            elements = driver.find_elements(by, value)
            return elements
        except StaleElementReferenceException:
            if i < retries - 1:
                time.sleep(1)
            else:
                raise

def search_lowes_selenium(query, store):
    driver = get_selenium_driver()
    if driver is None:
        return {"error": "Failed to initialize Selenium WebDriver."}

    try:
        # Navigate to the search page
        search_url = get_search_url(store, query)
        print(f"Navigating to URL: {search_url}")
        driver.get(search_url)

        wait = WebDriverWait(driver, 10)

        p_tag = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.typography.variant--body_1.align--left')))
        text_content = p_tag.text

        # Parse the number from the text content
        number_of_results = int(text_content.split()[0])
        print(f"Number of results: {number_of_results}")

        formatted_response = {"facets": [], "total_count": number_of_results, "facets_skipped": []}

        # Extract filters sections
        print(f"Number of results: {number_of_results}")
        filters_sections = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='sb']//div[@id]")))

        # Extract department data
        department_wrapper = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.deptl')))
        departments = safe_find_elements(department_wrapper, By.CSS_SELECTOR, '.showLeaf')
        department_data = []
        departments_heading = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-selector='splp-dpt-hd']"))).text
        for department in departments:
            name = safe_find_element(department, By.CSS_SELECTOR, 'h3').text
            count = safe_find_element(department, By.CSS_SELECTOR, '.prd-count').text.strip('()')
            department_data.append({"name": name, "count": count})
        formatted_response["facets"].append({
            "attrName": departments_heading,
            "values": department_data
        })
        try:
            time.sleep(5)
            for div_element in filters_sections:
                facet_name = extract_facet_name(div_element)
                print(f"Facet name: {facet_name}")
                facet_values = extract_facet_values(div_element, driver, formatted_response, facet_name)
                print(f"Facet values: {facet_values}")
                formatted_response["facets"].append({
                    "attrName": facet_name,
                    "values": facet_values
                })
        except Exception as e:
            print("Error extracting facet data", e)

        print(f"Formatted response: {formatted_response}")
        return formatted_response
    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        driver.quit()

def extract_total_count(container):
    """Extracts the total count from the items container."""
    try:
        total_count_element = container.get_attribute('data-totaltile')
        return int(total_count_element)
    except Exception as e:
        print(f"Error extracting total count: {e}")
        return 0

def extract_facet_name(section):
    """Extracts the facet name from a filter section."""
    try:
        return safe_find_element(section, By.CSS_SELECTOR, 'h2.facetTitle').text
    except Exception as e:
        print(f"Error extracting facet name: {e}")
        return ""

def extract_facet_values(section, driver, formatted_response, facet_name):
    """Extracts the facet values from a filter section."""
    facet_values = []
    try:
        try:
            accordion_button = safe_find_element(section, By.CSS_SELECTOR, '.accordion-header.closed')
            if accordion_button:
                accordion_button.click()
                time.sleep(2)
            else:
                print("No 'accordion closed' button found")
        except NoSuchElementException:
            pass
        try:
            see_all_button = safe_find_element(section, By.CSS_SELECTOR, '.link-start-icon')
            see_all_button.click()
            time.sleep(2)
        except NoSuchElementException:
            pass

        accordion_content = safe_find_element(section, By.CSS_SELECTOR, '.accordion-content')
        item_count_spans = safe_find_elements(accordion_content, By.CSS_SELECTOR, '.item-count')
        for item_count_span in item_count_spans:
            title = item_count_span.get_attribute('title')
            name, count = title.rsplit('(',1)
            count = count.strip(')')
            facet_values.append({"name": name, "count": count})
        if len(facet_values) == 0:
            formatted_response["facets_skipped"].append(facet_name)
    except Exception as e:
        formatted_response["facets_skipped"].append(facet_name)
        print(f"Error extracting facet values: {e}")
    return facet_values

if __name__ == "__main__":
    data = search_lowes_selenium("baseball bats")
    with open("lowes_facets.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Formatted response saved to lowes_facets.json")