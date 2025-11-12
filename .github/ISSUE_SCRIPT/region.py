#!/usr/bin/env python3
"""
Handler for region submissions.
"""

import argparse
import json
from pathlib import Path
import os

def set_arg_parser():
    """
    Creates an argument parser to take the submitted issue body as an argument.

        :returns: Argument parser.
    """
    parser = argparse.ArgumentParser(description="Run arguments")
    parser.add_argument("parsed_data", help="The field content parsed from the issue body.")
    args = parser.parse_args()
  
    return args

    
def validate_region(data):
    """
    Validate region submission.

        :param data: The field content of the issue body.
        :returns: Errors caused by missing or incorrectly formatted fields.
    """
    errors = []

    #Required fields
    required = ["validation_key", "label", "description", "id"]
    for field in required:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")
    
    #ID format check
    exp_id = data.get("experiment_id", "")
    if exp_id and not exp_id.islower():
        errors.append("Experiment ID must be lower case")
    if " " in exp_id:
        errors.append("Experiment ID cannot contain spaces")

    return errors

    
def create_region_json(data):
    """
    Create JSON file from parsed data.

        :param data: The field content of the issue body.
        :returns: Non metadata issue form content in the structure of a JSON 
        file. 
    """
    
    location_fields = {
        "latitude": "lat",
        "longitude": "lon",
        "city": "city",
        "country": "country"
    }

    location_dict = {}
    result = {}

    #Map fields from the issue form to JSON structure
    for key, value in data.items():
        #if key not in ["issue-type", "issue--kind"] and value:
            # Convert field names back to JSON format
            # json_key = key.replace("_", "-")
            result[key]=value
            
    if "type" in result:
        result["@type"] = result.pop("type")
    if "id" in result:
        result["@id"] = result.pop("id")
    # Add @context back into JSON        
    result["@context"] = "_context"

    # Recreate nested location dictionary
    for old_key, new_key in location_fields.items():
        if old_key in result:
            location_dict[new_key] = result.pop(old_key)
    if location_dict:
        result["location"] = location_dict

    return result

    
def run(parsed_data):
    """
    Main handler function.

        :param parsed_data: The field content parsed from the issue body.
        :returns: Output file status, name, category and ID as a dictionary.
    """
    print("processing region submission...")

    #Validate
    errors = validate_region(parsed_data)
    if errors:
        print("Validation errors:")
        for error in errors:
            print(f" - {error}")
        return {"success":False, "errors":errors}
    
    #Create JSON
    entry = create_region_json(parsed_data)

    #Write file
    output_dir = Path("region")
    output_dir.mkdir(exist_ok=True)

    entry_id = parsed_data.get("id", "unknown")
    output_file = output_dir / f"{entry_id}.json"

    with open(output_file, "w") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)
    print(f"Created: {output_file}")

    return {
        "success": True,
        "file": str(output_file),
        "category": "region",
        "id": entry_id
    }

    
if __name__ == "__main__":
     args = set_arg_parser()
     run(args.parsed_data)