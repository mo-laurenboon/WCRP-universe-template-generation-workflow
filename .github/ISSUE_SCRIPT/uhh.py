#!/usr/bin/env python3
"""
Handler for uhh submissions.
"""

import json
from pathlib import Path

def validate_uhh(data):
    """
    Validate uhh submission.

        :param data: The field content of the issue body.
        :returns: Errors caused by missing or incorrectly formatted fields.
    """
    errors = []

    #Required fields
    required = ["validation_key", "ui_label", "description", "id"]
    for field in required:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")
    
    #ID format check
    exp_id = data.get("id", "")
    if exp_id and not exp_id.islower():
        errors.append("Experiment ID must be lower case")
    if " " in exp_id:
        errors.append("Experiment ID cannot contain spaces")

    return errors

def create_uhh_json(data):
    """
    Create JSON file from parsed data.

        :param data: The field content of the issue body.
        :returns: non metadata issue form content in the structure of a JSON 
        file. 
    """
    result = {}

    #Map fields from the issue form to JSON structure
    for key, value in data.items():
        if key not in ["issue-type", "issue--kind"] and value:
            # Convert field names back to JSON format
            json_key = key.replace("_", "-")
            result[json_key]=value

    return result

def run(parsed_data, issue_data):
    """
    Main handler function.

        :param parsed_data: The field content parsed from the issue body.
        :param issue_data: The issue form as structured data.
        :returns: Output file status, name, category and ID as a dictionary.
    """
    print("processing uhh submission...")

    #Validate
    errors = validate_uhh(parsed_data)
    if errors:
        print("Validation errors:")
        for error in errors:
            print(f" - {error}")
        return {"success":False, "errors":errors}
    
    #Create JSON
    entry = create_uhh_json(parsed_data)

    #Write file
    output_dir = Path("uhh")
    output_dir.mkdir(exist_ok=True)

    entry_id = parsed_data.get("id", "unknown")
    output_file = output_dir / f"{entry_id}.json"

    with open(output_file, "w") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)
    print(f"Created: {output_file}")

    return {
        "success": True,
        "file": str(output_file),
        "category": "uhh",
        "id": entry_id
    }