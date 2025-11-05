from pathlib import Path
import json
import csv
from tqdm import tqdm


def scan_directories():
    """
    Iterates through all top-level directories in the repository and lists all 
    json files.

        :returns: A list of the paths of the form category/file.json for all 
        json files in the repository.
        :raises FileNotFoundError: If no JSON files are found.
        :raises PermissionError: If directory access is denied.
    """
    try:
        #get all subdirectories within the root directory
        categories = [d for d in Path(".").iterdir() 
                      if d.is_dir() and not d.name.startswith(".")]
    except PermissionError as e:
        raise PermissionError(f"Permission error accessing dictionaries: {e}.")
    
    files = []
    #scan each subdirectory for json files and append their path to list
    for cat in categories:
        jsons = cat.glob("*.json")
        for j in jsons:
            files.append(j)
    
    if not files:
        raise FileNotFoundError("No JSON files found.")

    return categories, files


def get_all_json_keys(files): # may require removal if not used --------------------------------------------------------------------
    """
    Lists all unique keys within the found JSON files.

        :param files: A list of the paths for all json files in the repository.
        :returns: A list of all unique keys within the found JSON files.
        :raises ValueError: If no keys are found.
    """
    keys = []
    for file in files:
        #load each json file
        with file.open("r", encoding="utf-8") as f:
            data = json.load(f)
            #append any key not already listed
            for key, _ in data.items():
                if key not in keys:
                    keys.append(key)
    if not keys:
        raise ValueError("No keys found within JSON files.")
    #print the list of unique keys
    print(f"\n{len(keys)} unique keys found across all JSON files...")
    for key in keys:
        print(f"- {key}")

    return keys


def record_instances_of_keys(categories, keys): # may require removal if not used --------------------------------------------------
    """
    Prints a list of keys found within the JSON files of a given subdirectory 
    (category).

        :param categories: A list of subdirectories found in the repository.
        :param keys: A list of all unique keys within the found JSON files.
    """
    for cat in categories:
        jsons = cat.glob("*.json")
        for j in jsons:
            #load each json with the current subdirectory
            with j.open("r", encoding="utf-8") as f:
                data = json.load(f)
                #create a list of all unique keys within that subdirectory only
                filename = f"found_keys_{cat}"
                filename = []
                for key in keys:
                    if key in data and key not in filename:
                        filename.append(key)
        print(f"The keys found in the {cat} category files are:", filename)
        #clear list ready for the next subdirectory
        filename.clear()


def flatten_nested_dictionaries(dictionary, parent_key='', sep='_'):
    """
    Flattens any nested dictionaries into separate key value items.

        :param dictionary: The dictionary to flatten.
        :param parent_key: The parent key.
        :param sep: Key name separator.
        :raises FileNotFoundError: If the provided dictionary cannot be found.
        :returns: Flattened dictionary.
    """
    if not dictionary:
        raise FileNotFoundError("This dictionary does not exist")
    items = []
    #each key check if the value is a another dictionary, list or a set value
    for k, v in dictionary.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            #flatten nested dictionary to create a new parent key-value pair
            items.extend(flatten_nested_dictionaries(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            items.append((new_key, ', '.join(map(str, v))))
        else:
            items.append((new_key, v))

    return dict(items)


def create_csv(files, out_directory):
    """
    Creates a unique csv for each json file based off of its structure.

        :param files: A list of the paths for all json files in the repository.
        :param out_directory: The directory to output the created csv files.
    """
    headers = ["field_order","field_type","field_id","label","description",
               "data_source","required","placeholder","options_type",
               "default_value"]
    
    #open progress bar loop
    for file in tqdm(files, desc="Creating csv files...", unit="file", 
                     dynamic_ncols=True):
        keys = []
        output_csv_filename = f"{file.stem}.csv"
        output_csv = out_directory / output_csv_filename
        with file.open("r", encoding="utf-8") as f:
            dictionary = json.load(f)
            data = flatten_nested_dictionaries(dictionary, parent_key='',
                                                    sep='_')
            for key, _ in data.items():
                #get a list of the keys within the json file
                if key not in keys:
                    keys.append(key)
            with open("master_csv_template.csv", mode="r", newline="") as infile:
                reader = csv.reader(infile)
                with open(output_csv, mode='w', newline='') as outfile:
                    writer = csv.writer(outfile)
                    #copy data with matching keys from the master csv
                    data = [row for row in reader if row[1] in keys] 
                    #copy column headers to the csv data                         
                    data.insert(0, headers)  
                    for i in range(1, len(data)):
                        data[i].insert(0, i)          
                    for row in data:
                        writer.writerow(row)


def create_hardcoded_python_files(files, out_directory):
    """
    Creates a hard coded unique python for each json file based off of its 
    structure.

        :param files: A list of the paths for all json files in the repository.
        :param out_directory: The directory to output the created python files.
    """
    #open progress bar loop
    for file in tqdm(files, desc="Creating python files...", unit="file", 
                     dynamic_ncols=True):
        output_python_filename = f"{file.stem}.py"
        output_python = out_directory / output_python_filename
        #write uniquely named python file for each json file
        with open(output_python, "w") as outfile:
            #created hardcoded python structure, swap for cmipld at a later date
            outfile.write(
"""
TEMPLATE_CONFIG = {
    "name": "Experiment Submission",
    "description": "Submit a new experiment definition",
    "title": "[EXPERIMENT] New Submission",
    "labels": ["experiment", "cv-submission"]
}

DATA = {
    "issue_types": ["new", "modify", "delete"],
    "types": {
        "wcrp": {"id": "wcrp", "label": "wcrp"},
        "esgvoc": {"id": "esgvoc", "label": "esgvoc"},
        "universal": {"id": "universal", "label": "universal"}
    },
    "realms": {
        "atmos": {"id": "atmos", "label": "atmos"},
        "land": {"id": "land", "label": "land"},
        "ocean": {"id": "ocean", "label": "ocean"},
        "ocnbgchem": {"id": "ocnbgchem", "label": "ocnbgchem"},
        "seaice": {"id": "seaice", "label": "seaice"}
    }
}
"""
            )


def create_dynamic_python_files(files, out_directory): #may not be used, reveiw before final submission ==================================
    """
    Dynamically creates a unique python for each json file based off of its 
    structure using the cmip-ld library.

        :param files: A list of the paths for all json files in the repository.
        :param out_directory: The directory to output the created python files.
    """
    #open progress bar loop
    for file in tqdm(files, desc="Creating python files...", unit="file",
                  leave=False, dynamic_ncols=True):
        output_python_filename = f"{file.stem}.py"
        output_python = out_directory / output_python_filename
        #write uniquely named python file for each json file
        with open(output_python, "w") as outfile:
            #created hardcoded python structure, swap for cmipld at a later date
            outfile.write(
"""
import cmipld
from cmipld.utils.ldparse import name_multikey_extract

TEMPLATE_CONFIG = {
    "name": "Experiment Submission",
    "description": "Submit a new experiment definition",
    "title": "[EXPERIMENT] New Submission",
    "labels": ["experiment", "cv-submission"]
}

DATA = {
    "issue_types": ["new", "modify", "delete"],
    "activities": name_multikey_extract(
        cmipld.get("universal:activity/graph.jsonld")["@graph"],
        ["id", "validation-key", "ui-label"],
        "validation-key"
    ),
    "experiments": name_multikey_extract(
        cmipld.get("universal:experiment/graph.jsonld")["@graph"],
        ["id", "validation-key", "ui-label"],
        "validation-key"
    ),
    "types": {
        "wcrp": {"id": "wcrp", "label": "wcrp"},
        "esgvoc": {"id": "esgvoc", "label": "esgvoc"},
        "universal": {"id": "universal", "label": "universal"}
    },
    "realms": {
        "atmos": {"id": "atmos", "label": "atmos"},
        "land": {"id": "land", "label": "land"},
        "ocean": {"id": "ocean", "label": "ocean"},
        "ocnbgchem": {"id": "ocnbgchem", "label": "ocnbgchem"},
        "seaice": {"id": "seaice", "label": "seaice"}
    }
}
"""
            )


def main():
    """
    Holds the main body of the script.
    """
    #Get information on repository and JSON file structure
    categories, files = scan_directories()
    keys = get_all_json_keys(files)
    record_instances_of_keys(categories, keys)

    #Create required files
    out_directory = Path(".github") / "GEN_ISSUE_TEMPLATE"
    out_directory.mkdir(parents=True, exist_ok=True)
    create_csv(files, out_directory)
    create_hardcoded_python_files(files, out_directory)
    

if __name__ == "__main__":
    main()