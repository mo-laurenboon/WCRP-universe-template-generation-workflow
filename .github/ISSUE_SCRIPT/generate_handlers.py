#!/ usr /bin /env python3
"""
Auto - generate issue handler scripts
"""

from pathlib import Path
from jinja2 import Template
from tqdm import tqdm 

HANDLER_TEMPLATE = '''#!/usr/bin/env python3
"""
Handler for {{ category }} submissions.
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

def validate_{{ category_safe }}(data):
    """
    Validate {{ category }} submission.

        :param data: The field content of the issue body.
        :returns: Errors caused by missing or incorrectly formatted fields.
    """
    errors = []

    #Required fields
    required = ["validation_key", "label", "description", "experiment_id"]
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

def create_{{ category_safe }}_json(data):
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
            if key == "type":
                dictionary["@type"] = dictionary.pop("type")
            if key == "id":
                dictionary["@id"] = dictionary.pop("id")
            # Convert field names back to JSON format
            json_key = key.replace("_", "-")
            result[json_key]=value
    result["@context"] = "_context"

    return result

def run(parsed_data):
    """
    Main handler function.

        :param parsed_data: The field content parsed from the issue body.
        :returns: Output file status, name, category and ID as a dictionary.
    """
    print("processing {{ category }} submission...")

    #Validate
    errors = validate_{{ category_safe }}(parsed_data)
    if errors:
        print("Validation errors:")
        for error in errors:
            print(f" - {error}")
        return {"success":False, "errors":errors}
    
    #Create JSON
    entry = create_{{ category_safe }}_json(parsed_data)

    #Write file
    output_dir = Path("{{ category }}")
    output_dir.mkdir(exist_ok=True)

    entry_id = parsed_data.get("id", "unknown")
    output_file = output_dir / f"{entry_id}.json"

    with open(output_file, "w") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)
    print(f"Created: {output_file}")

    return {
        "success": True,
        "file": str(output_file),
        "category": "{{ category }}",
        "id": entry_id
    }

if __name__ == "__main__":
     args = set_arg_parser()
     run(args.parsed_data)
'''

def generate_handlers():
    """
    Generate handler scripts for all categories.
    """
    gen_template_dir = Path(".github/GEN_ISSUE_TEMPLATE")
    output_dir = Path(".github/ISSUE_SCRIPT")
    output_dir.mkdir(parents=True, exist_ok=True)

    #get all csv files (expected one per category)
    csv_files = list(gen_template_dir.glob("*.csv"))
    template = Template(HANDLER_TEMPLATE)

    for csv_file in tqdm(csv_files, desc="Creating handler scripts...", unit="file", 
                         dynamic_ncols=True):
        category = csv_file.stem
        category_safe = category.replace("-", "_")

        handler_content  = template.render(
            category = category,
            category_safe = category_safe
        )

        output_file = output_dir / f"{category}.py"
        with open(output_file, "w") as f:
            f.write(handler_content)
        
        output_file.chmod(0o755)
        tqdm.write(f"Generated: {output_file}")

    print(f"\nCreated {len(csv_files)} handler scripts.")

if __name__ == "__main__":
    generate_handlers()
