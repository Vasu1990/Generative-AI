import json

def extract_data_from_json_tractor_supply(json_response):
    """Extracts relevant product and facet data from a JSON response."""
    extracted_data = {"products": [], "facets": [],
                      "total_count": json_response.get("metaData", {}).get("resultsFound")}

    def is_product_filter(facet):
        """Determine if a facet is a meaningful product filter"""
        # Skip facets with non-product values
        if not facet.get("entry"):
            return False
            
        # Check if values are meaningful product attributes
        values = facet.get("entry", [])
        if not values:
            return False
            
        # Skip if values are just IDs or system values
        first_value = values[0].get("label", "")
        if "_" in first_value or first_value.startswith("http"):
            return False
            
        # Skip facets with only one value
        if len(values) <= 1:
            return False

        return True

    # Extract facet information
    if "facetView" in json_response and isinstance(json_response["facetView"], list):
        for facet in json_response["facetView"]:
            if not is_product_filter(facet):
                continue
                
            facet_name = facet.get("name", "")
            facet_data = {
                "attrName": facet_name,
                # "attrIdentifier": facet.get("attrIdentifier"),
                "values": []
            }

            if "entry" in facet and isinstance(facet["entry"], list):
                for value_item in facet["entry"]:
                    if value_item.get("label") and value_item.get("count", 0) > 0:
                        facet_value_data = {
                            "value": value_item["label"].strip(),
                            "count": value_item["count"]
                        }
                        facet_data["values"].append(facet_value_data)

            if facet_data["values"]:  # Only add if there are values
                extracted_data["facets"].append(facet_data)
            
    return extracted_data