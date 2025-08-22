import json

def extract_data_from_json_dicks(json_response):
    """Extracts relevant product and facet data from a JSON response."""
    extracted_data = {
        "products": [],
        "facets": [],
        "total_count": None
    }

    # Extract total count
    extracted_data["total_count"] = json_response.get("totalCount")

    def is_product_filter(facet):
        """Determine if a facet is a meaningful product filter"""
        # Skip system or navigational facets
        skip_identifiers = {'facetCatgroup', 'forcesync'}
        if facet.get("attrIdentifier") in skip_identifiers:
            return False
            
        # Skip facets with non-product values
        if not facet.get("valueList"):
            return False
            
        # Check if values are meaningful product attributes
        values = facet.get("valueList", [])
        if not values:
            return False
            
        # Skip if values are just IDs or system values
        first_value = values[0].get("value", "")
        if "_" in first_value or first_value.startswith("http"):
            return False
            
        # Skip facets with only one value
        if len(values) <= 1:
            return False

        return True

    # Extract facet information
    if "facetVOs" in json_response and isinstance(json_response["facetVOs"], list):
        for facet in json_response["facetVOs"]:
            if not is_product_filter(facet):
                continue
                
            facet_name = facet.get("attrName", "")
            facet_data = {
                "attrName": facet_name,
                "attrIdentifier": facet.get("attrIdentifier"),
                "values": []
            }

            if "valueList" in facet and isinstance(facet["valueList"], list):
                for value_item in facet["valueList"]:
                    if value_item.get("value") and value_item.get("count", 0) > 0:
                        facet_value_data = {
                            "value": value_item["value"].strip(),
                            "count": value_item["count"]
                        }
                        facet_data["values"].append(facet_value_data)

            if facet_data["values"]:  # Only add if there are values
                extracted_data["facets"].append(facet_data)
            
    return extracted_data