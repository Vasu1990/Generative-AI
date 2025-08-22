def extract_data_from_json_home_depot(json_response):
    """Extracts relevant product and facet data from a JSON response."""
    extracted_data = {"products": [], "facets": [], "total_count": json_response.get("total_count"),
                      "facets_skipped": json_response.get("facets_skipped")}

    # Extract facet information
    facets = json_response.get("facets", [])
    for facet in facets:
        facet_name = facet.get("attrName", "")
        facet_data = {
            "attrName": facet_name,
            "values": []
        }

        if "values" in facet and isinstance(facet["values"], list):
            for value_item in facet["values"]:
                if value_item.get("name") and value_item.get("count") is not None:
                    facet_value_data = {
                        "value": value_item["name"].strip(),
                        "count": value_item["count"]
                    }
                    facet_data["values"].append(facet_value_data)

        if facet_data["values"]:  # Only add if there are values
            extracted_data["facets"].append(facet_data)

    return extracted_data