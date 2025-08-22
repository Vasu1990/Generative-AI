import os
import streamlit as st
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from scrapers.dicks.dicks_scraper import search_dicks_sporting
from scrapers.academy.academy_scraper import search_academy
from processors.dicks.dicks_processor import extract_data_from_json_dicks
from processors.academy.academy_processor import extract_data_from_json_academy
from utils.logger import app_logger, ai_logger
from utils.ai_analyzer import generate_analysis
from scrapers.tractor_supply.tractor_supply_scraper import search_tractor_supply
from processors.tractor_supply.tractor_supply_processor import extract_data_from_json_tractor_supply
from scrapers.amazon.amazon_scraper_selenium import search_amazon_selenium  # Use Selenium scraper
from scrapers.lowes.lowes_scraper_selenium import search_lowes_selenium
from processors.lowes.lowes_processor import extract_data_from_json_lowes
from processors.walmart.walmart_processor import extract_data_from_json_walmart
from scrapers.walmart.walmart_scraper_selenium import search_walmart_selenium
from scrapers.home_depot.home_depot_scraper_selenium import search_home_depot_selenium
from processors.home_depot.home_depot_processor import extract_data_from_json_home_depot
from utils.url_utils import get_search_url

# Load config file
with open('config/category-vendor.json', 'r') as f:
    config = json.load(f)

with open('config/all-stores.json', 'r') as f:
    stores = json.load(f)

CATEGORY_STORE_MAPPING = config["CATEGORY_STORE_MAPPING"]
ALL_STORES = sorted(stores["ALL_STORES"])

def combine_facets(store_data, academy_data):
    """Combine facets from the store and Academy"""
    return {
        "total_count": {
            "Store": store_data.get("total_count", 0),
            "Academy": academy_data.get("total_count", 0)
        },
        "facets": {
            "Store": store_data.get("facets", []),
            "Academy": academy_data.get("facets", [])
        },
        "facets_skipped": {
            "Store": store_data.get("facets_skipped", []),
            "Academy": academy_data.get("facets_skipped", [])
        },
        "errors": {
            "Store": store_data.get("errors", []),
            "Academy": academy_data.get("errors", [])
        },
        "no_result": store_data.get("no_result", False)
    }

def display_insights(combined_data, search_term, store_name):
    """Display AI-generated insights"""
    try:
        ai_logger.info(f"Starting analysis for search term: {search_term} for store: {store_name}")

        with st.spinner(f"Analyzing competitive data using Gemini AI for {store_name}..."):
            # Check if using single prompt or multiple prompts
            use_single_prompt = os.getenv('USE_SINGLE_PROMPT', 'true').lower() == 'true'

            if use_single_prompt:
                # Generate analysis using a single prompt
                analysis = generate_analysis(combined_data, search_term, store_name)

                if not analysis:
                    st.error("Failed to generate insights. Please try again.")
                    return

                # Create tabs for different sections
                overview_tab, details_tab, recommendations_tab = st.tabs([
                    "Key Findings",
                    "Detailed Analysis",
                    "Recommendations"
                ])

                # Display the analysis in tabs
                with overview_tab:
                    st.markdown("### Key Findings")
                    if "## Key Findings" in analysis:
                        findings = analysis.split("## Key Findings")[1].split("## Detailed Analysis")[0]
                        st.markdown(findings, unsafe_allow_html=True)
                        log_file_path = os.path.join(os.path.dirname(__file__), f'{store_name}_Key_Finding.log')
                        with open(log_file_path, 'w') as log_file:
                            log_file.write(findings)
                    else:
                        st.warning("Key Findings section not found in the analysis.")

                with details_tab:
                    st.markdown("### Detailed Analysis")
                    if "## Detailed Analysis" in analysis:
                        details = analysis.split("## Detailed Analysis")[1].split("## Recommendations")[0]
                        st.markdown(details, unsafe_allow_html=True)
                        # Write detailed analysis to a log file
                        log_file_path = os.path.join(os.path.dirname(__file__), f'{store_name}_{search_term}_detailed_analysis.log')
                        with open(log_file_path, 'w') as log_file:
                            log_file.write(details)
                    else:
                        st.warning("Detailed Analysis section not found in the analysis.")

                with recommendations_tab:
                    st.markdown("### Recommendations")
                    if "## Recommendations" in analysis:
                        recommendations = analysis.split("## Recommendations")[1]
                        st.markdown(recommendations, unsafe_allow_html=True)
                        log_file_path = os.path.join(os.path.dirname(__file__), f'{store_name}_recommendations.log')
                        with open(log_file_path, 'w') as log_file:
                            log_file.write(recommendations)
                    else:
                        st.warning("Recommendations section not found in the analysis.")

                # Add download button for the analysis
                if st.download_button(
                    label="Download Analysis",
                    data=analysis,
                    file_name=f"competitive_analysis_{search_term}_{store_name}.md",
                    mime="text/markdown"
                ):
                    st.success("File downloaded successfully!")

            else:
                # Generate analysis for each section
                key_findings = generate_analysis(combined_data, search_term, store_name, "key_findings")
                detailed_analysis = generate_analysis(combined_data, search_term, store_name, "detailed_analysis")
                recommendations = generate_analysis(combined_data, search_term, store_name, "recommendations")

                # Create tabs for different sections
                overview_tab, details_tab, recommendations_tab = st.tabs([
                    "Key Findings",
                    "Detailed Analysis",
                    "Recommendations"
                ])

                # Display the analysis in tabs
                with overview_tab:
                    st.markdown(key_findings, unsafe_allow_html=True)

                with details_tab:
                    st.markdown(detailed_analysis, unsafe_allow_html=True)

                with recommendations_tab:
                    st.markdown(recommendations, unsafe_allow_html=True)

                # Add download button for the analysis
                full_analysis = f"### Key Findings\n{key_findings}\n\n### Detailed Analysis\n{detailed_analysis}\n\n### Recommendations\n{recommendations}"
                # Write detailed analysis to a log file
                log_file_path = os.path.join(os.path.dirname(__file__), f'{store_name}_{search_term}_final_analysis.log')
                with open(log_file_path, 'w') as log_file:
                    log_file.write(full_analysis)

                if st.download_button(
                    label="Download Analysis",
                    data=full_analysis,
                    file_name=f"competitive_analysis_{search_term}_{store_name}.md",
                    mime="text/markdown"
                ):
                    st.success("File downloaded successfully!")
            
    except Exception as e:
        error_msg = f"Error generating insights: {str(e)}"
        ai_logger.error(error_msg)
        st.error(error_msg)

def display_results(combined_data, search_term, store_name):
    """Display search results and insights"""
    # Create columns for metrics and insights button
    col1, col2, col3 = st.columns([2, 2, 1])
    
    # Display metrics
    with col1:
        store_total_count = combined_data["total_count"]["Store"]
        if store_name == "Walmart" and store_total_count == 1000:
            store_total_count_display = "1000+"
        else:
            store_total_count_display = store_total_count
        st.metric(f"{store_name} Total Products", store_total_count_display)
    with col2:
        st.metric("Academy Total Products", combined_data["total_count"]["Academy"])
    with col3:
        unique_key = f"insights_button-{store_name}-{search_term}"
        if st.button(f"🔍 Get Insights for {store_name}", key=unique_key):
            st.session_state[f"show_insights-{store_name}-{search_term}"] = True
            app_logger.info(f"User requested insights analysis for {store_name}")

    # Show insights if requested
    if st.session_state.get(f"show_insights-{store_name}-{search_term}", False):
        st.session_state[f"show_insights-{store_name}-{search_term}"] = False  # Reset the state
        st.markdown("---")  # Add separator
        display_insights(combined_data, search_term, store_name)
        st.markdown("---")  # Add separator

    # Display facets
    st.subheader(f"Available Filters for {store_name}")
    skipped_filters = combined_data["facets_skipped"]["Store"]
    if len(skipped_filters) > 0:
        st.markdown(f'<div style="background-color: #B3D9FF; padding: 10px; border-radius: 5px; font-size: 14px;">'
                f'<b>Could not process below Facets {store_name} </b>: <br>'  # Add a line break after the title
                f'{("<br>".join(skipped_filters)) if skipped_filters else "None"}'
                f'</div>',unsafe_allow_html=True)
        
    if store_name == "Dick's" or store_name == "Tractor Supply":
        st.info(f"{store_name} Facets are retrieved via an API and may not perfectly match the website.")

    # Display errors if any
    errors = combined_data["errors"]["Store"]
    if len(errors) > 0:
        st.error(f"#### Errors for {store_name} : {', '.join(errors)}")

    # Display no results message if applicable
    if combined_data["no_result"]:
        search_url = get_search_url(store_name, search_term)
        st.error(f"Unable to scrape {store_name}. Please visit {search_url} to verify.")

    # Create two columns for side-by-side display
    store_col, academy_col = st.columns(2)

    with store_col:
        search_url = get_search_url(store_name, search_term)
        st.markdown(f'<h3><a href="{search_url}" target="_blank">{store_name}</a></h3>', unsafe_allow_html=True)
        for facet in sorted(combined_data["facets"]["Store"], key=lambda x: x["attrName"]):
            with st.expander(f"{facet['attrName']} ({len(facet['values'])} options)"):
                sorted_values = sorted(facet["values"], key=lambda x: x["count"] if isinstance(x, dict) and "count" in x else 0, reverse=True)
                for value in sorted_values:
                    if isinstance(value, dict) and "value" in value and "count" in value:
                        st.write(f"• {value['value']} ({value['count']} items)")
                    else:
                        st.write(f"• {value}")

    with academy_col:
        search_url = get_search_url("Academy", search_term)
        st.markdown(f'<h3><a href="{search_url}" target="_blank">Academy Sports</a></h3>', unsafe_allow_html=True)
        for facet in sorted(combined_data["facets"]["Academy"], key=lambda x: x["attrName"]):
            with st.expander(f"{facet['attrName']} ({len(facet['values'])} options)"):
                sorted_values = sorted(facet["values"], key=lambda x: x["count"] if isinstance(x, dict) and "count" in x else 0, reverse=True)
                for value in sorted_values:
                    if isinstance(value, dict) and "value" in value and "count" in value:
                        st.write(f"• {value['value']} ({value['count']} items)")
                    else:
                        st.write(f"• {value}")

def handle_no_results(store, aso_data):
    """Handle the case where no results are found."""
    return combine_facets({"no_result": True}, aso_data)

def scrape_store(store, search_term, aso_data):
    """Scrape data for a specific store and combine with Academy data."""
    try:
        if store == "Dick's":
            results = search_dicks_sporting(search_term=search_term, store=store)
            if results:
                data = extract_data_from_json_dicks(results)
                return store, combine_facets(data, aso_data)
            else:
                return store, handle_no_results(store, aso_data)
        elif store == "Tractor Supply":
            results = search_tractor_supply(query=search_term)
            if results:
                data = extract_data_from_json_tractor_supply(results)
                return store, combine_facets(data, aso_data)
            else:
                return store, handle_no_results(store, aso_data)
        elif store == "Walmart":
            results = search_walmart_selenium(query=search_term, store=store)
            if results:
                data = extract_data_from_json_walmart(results)
                return store, combine_facets(data, aso_data)
            else:
                return store, handle_no_results(store, aso_data)
        elif store == "Amazon":
            results = search_amazon_selenium(query=search_term, store=store)
            if results:
                return store, combine_facets(results, aso_data)
            else:
                return store, handle_no_results(store, aso_data)
        elif store == "Lowe's":
            results = search_lowes_selenium(query=search_term, store=store)
            if results:
                data = extract_data_from_json_lowes(results)
                return store, combine_facets(data, aso_data)
            else:
                return store, handle_no_results(store, aso_data)
        elif store == "Home Depot":
            results = search_home_depot_selenium(query=search_term, store=store)
            if results:
                data = extract_data_from_json_home_depot(results)
                return store, combine_facets(data, aso_data)
            else:
                return store, handle_no_results(store, aso_data)
        # Add other store search methods here as needed
    except Exception as e:
        app_logger.error(f"Error scraping {store}: {str(e)}")
        return store, combine_facets({"errors": [str(e)]}, aso_data)
    return store, None

def generate_cache_key(store, search_term):
    """Generate a cache key based on store and search term."""
    return f"{store}-{search_term}-vs_Academy"

def update_displayed_results(cache_key, combined_data, search_term, store):
    """Update displayed results and session state."""
    display_results(combined_data, search_term, store)
    st.session_state.displayed_results.add(cache_key)
    st.markdown("<hr><br>", unsafe_allow_html=True)

def main():
    st.title("Competitive Search Analysis")

    # Initialize session state
    if 'combined_data' not in st.session_state:
        st.session_state.combined_data = []
    if 'show_insights' not in st.session_state:
        st.session_state.show_insights = {}
    if 'displayed_results' not in st.session_state:
        st.session_state.displayed_results = set()
    if 'executor' not in st.session_state:
        st.session_state.executor = None

    # Create input fields
    category = st.selectbox("Select Relevant Category for your Search Term (optional)", options=["Select Category"] + list(CATEGORY_STORE_MAPPING.keys()), placeholder="Select Category")

    # Display the "Search Term" label with a red asterisk
    st.markdown('Search Term <span style="color:red;">*</span>', unsafe_allow_html=True)
    search_term = st.text_input("Search Term", value="baseball bats", label_visibility="collapsed")

    # Display the "Select Stores" label with a red asterisk
    st.markdown('Select Stores <span style="color:red;">*</span>', unsafe_allow_html=True)

    # Determine store options based on selected category
    if category and category != "Select Category":
        default_stores = CATEGORY_STORE_MAPPING.get(category, [])
        selected_stores = st.multiselect(
            "Select Stores",
            options=ALL_STORES,
            default=default_stores,
            label_visibility="collapsed",
            placeholder="Select Store"
        )
    else:
        selected_stores = st.multiselect(
            "Select Stores",
            options=ALL_STORES,
            label_visibility="collapsed",
            placeholder="Select Store"
        )


    # Check if search term and stores are filled
    search_disabled = not search_term or not selected_stores
    # Search button
    if st.button("Search", disabled=search_disabled):
        
        #kill all active threads
        if st.session_state.executor:
            st.session_state.executor.shutdown(wait=False, cancel_futures=True)
            st.session_state.executor = None
            # st.info("Terminated previous searched. Starting new search...")

        app_logger.info(f"Searching for term: {search_term}")
        with st.spinner("Searching stores...please wait for it to complete before starting a new search"):
            try:
                # Search Academy once
                cache_key_Academy = generate_cache_key("Academy", search_term)
                if not any(d['cache_key'] == cache_key_Academy for d in st.session_state.combined_data):
                    aso_results = search_academy(search_term=search_term)
                    if not aso_results:
                        app_logger.warning("No results found at Academy")
                        aso_data = {}
                    else:
                        aso_data = extract_data_from_json_academy(aso_results)
                    st.session_state.combined_data.append({'cache_key': cache_key_Academy, 'data': aso_data})
                else:
                    aso_data = next(d['data'] for d in st.session_state.combined_data if d['cache_key'] == cache_key_Academy)
                 
                # Use ThreadPoolExecutor for parallel execution
                st.session_state.executor = ThreadPoolExecutor()
                future_to_store = {}
                for store in selected_stores:
                    cache_key = generate_cache_key(store, search_term)
                    cached_data = next((d['data'] for d in st.session_state.combined_data if d['cache_key'] == cache_key), None)

                    if cached_data and (cached_data.get("errors", {}).get("Store") or cached_data.get("no_result")):
                        app_logger.warning(f"Cache has error for {store}")
                        st.session_state.combined_data = [d for d in st.session_state.combined_data if d['cache_key'] != cache_key]
                        future_to_store[st.session_state.executor.submit(scrape_store, store, search_term, aso_data)] = store
                    elif cached_data:
                        update_displayed_results(cache_key, cached_data, search_term, store)
                        app_logger.info(f"Results for {store} and search term '{search_term}' already exist")
                    else:
                        future_to_store[st.session_state.executor.submit(scrape_store, store, search_term, aso_data)] = store

                for future in as_completed(future_to_store):
                    store = future_to_store[future]
                    try:
                        store, combined_data = future.result()
                        if combined_data:
                            cache_key = generate_cache_key(store, search_term)
                            st.session_state.combined_data.append({'cache_key': cache_key, 'data': combined_data})
                            st.session_state.show_insights[cache_key] = False
                            app_logger.info(f"Search completed successfully for {store}")
                            # Display results immediately after processing
                            update_displayed_results(cache_key, combined_data, search_term, store)
                        else:
                            app_logger.warning(f"No results found at {store}")
                    except Exception as e:
                        app_logger.error(f"Error processing {store}: {str(e)}")

            except Exception as e:
                error_msg = f"Error during search: {str(e)}"
                app_logger.error(error_msg)
                st.error(error_msg)
        st.rerun()

    for store in selected_stores:
        cache_key = generate_cache_key(store, search_term)
        if any(d['cache_key'] == cache_key for d in st.session_state.combined_data):
            combined_data = next(d['data'] for d in st.session_state.combined_data if d['cache_key'] == cache_key)
            update_displayed_results(cache_key, combined_data, search_term, store)
    # st.write(st.session_state)

if __name__ == "__main__":
    main()
