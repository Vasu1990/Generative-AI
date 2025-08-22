import json

def extract_data_from_json_academy(json_response):
    """Extracts relevant product and facet data from Academy Sports + Outdoors JSON response."""
    extracted_data = {
        "products": [],
        "facets": [],
        "total_count": None,
        "facet_display_name_map": {}
    }

    def is_product_filter(facet_name, facet_values):
        """Determine if a facet is a meaningful product filter"""
        # Only include facets that start with 'facet_'
        if not facet_name.startswith('facet_'):
            return False
            
        # Skip facets with only one value
        if len(facet_values) <= 1:
            return False
            
        # Skip if values look like IDs or system values
        first_value = next(iter(facet_values.items()))[0] if facet_values else ""
        if first_value.isdigit() or first_value.startswith('http'):
            return False

        return True

    def get_facet_display_name(facet_name, facet_display_name_map):
        """Get clean display name for a facet"""
        # Remove 'facet_' prefix
        name = facet_name.replace('facet_', '').capitalize()

        # Use the display name from the map if available
        if facet_name in facet_display_name_map:
            return facet_display_name_map[facet_name]

        return name

    # Extract facetNames from customUserData
    if "customUserData" in json_response:
        extracted_data["total_count"] = json_response["nbHits"]
        custom_user_data = json_response["customUserData"]
        user_data = json_response["userData"]
        # Extract facetDisplayNameMap
        if user_data and isinstance(user_data, list) and "facetDisplayNameMap" in user_data[0]:
            extracted_data["facet_display_name_map"] = user_data[0]["facetDisplayNameMap"]

        if "facetNames" in custom_user_data and "facets" in custom_user_data:
                facet_names = custom_user_data["facetNames"]
                facets = custom_user_data["facets"]
                for facet_key, facet_values in facet_names.items():
                    if facet_key in facets:
                        # Get appropriate display name
                        display_name = get_facet_display_name(facet_key, extracted_data["facet_display_name_map"])
                        facet_data = {
                            "attrName": display_name,
                            "attrIdentifier": facet_key,
                            "values": []
                        }
                        for facet_value in facets[facet_key]:
                            for value, count in facet_value.items():
                                if value and count > 0:
                                    facet_value_data = {
                                        "value": value.strip(),
                                        "count": count
                                    }
                                    facet_data["values"].append(facet_value_data)
                        if facet_data["values"]:  # Only add if there are values
                            extracted_data["facets"].append(facet_data)

    return extracted_data