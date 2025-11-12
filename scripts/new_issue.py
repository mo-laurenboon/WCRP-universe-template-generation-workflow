import os
import json
import sys
import importlib.util


path = '.github/ISSUE_SCRIPT/'


def get_issue():
    """
    Extracts information from the submitted issue.

        :returns: Issue body, labels, number, title and author as a dictionary.
    """
    return {
        'body': os.environ.get('ISSUE_BODY'),
        "labels_full": os.environ.get('ISSUE_LABELS'),
        'number': os.environ.get('ISSUE_NUMBER'),
        'title': os.environ.get('ISSUE_TITLE'),
        'author': os.environ.get('ISSUE_SUBMITTER')
    }


def parse_issue_body(issue_body):
    """
    Parses and cleans issue body contents to dictionary format.

        :param issue_body: The body of the submitted issue form.
        :returns: Issue body data in dictionary format.
    """
    lines = issue_body.split('\n')
    issue_data = {}
    current_key = None

    # Identify key-value pairs using markdown structure
    for line in lines:
        if line.startswith('### '):
            current_key = line[4:].strip().replace(' ', '_').lower()
            issue_data[current_key] = ''
        elif current_key:
            issue_data[current_key] += line.strip() + ' '

    # Remove trailing spaces
    for key in issue_data:
        issue_data[key] = issue_data[key].strip()

        if issue_data[key] == "\"none\"":
            issue_data[key] = issue_data[key].replace("\"none\"", "none")

    print(json.dumps(issue_data, indent=2))

    return issue_data


def main():
    """
    Holds the main body of the script.
    """
    # Generate handler script name from issue title
    issue = get_issue()
    issue_title = issue['title']
    parts = issue_title.split(":")
    if len(parts) > 2:
        script_name = parts[1].strip().lower()

    # Ensure an issue type is selected
    parsed_issue = parse_issue_body(issue['body'])
    print(parsed_issue)
    issue_type = parsed_issue.get('issue_type', '')
    print(json.dumps(parsed_issue,indent=4))
    if not issue_type:
        print(json.dumps(parsed_issue, indent=4))
        sys.exit('No issue type selected. Exiting.')

    # Define the path to the script based on the script_name
    script_path = f"{path}{script_name}.py"
    print(script_path)

    # Check if the script exists
    if os.path.exists(script_path):
        # Load the script dynamically
        spec = importlib.util.spec_from_file_location(issue_type, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"Successfully loaded {script_path}")
        # run the processing/handler script
        module.run(parsed_issue)

    else:
        sys.exit(f"Script: {script_path} does not exist. Exiting.")

if __name__ == "__main__":
    main()