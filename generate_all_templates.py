from pathlib import Path
import json
import csv

def scan_directories():
    """
    Scans all directories in the respository.

        :returns: The directories (categories) as a list.
    """
    categories = [d for d in Path(".").iterdir() 
                  if d.is_dir() and not d.name.startswith(".")]
    count = 0
    files = []
    for cat in categories:
        jsons = cat.glob("*.json")
        for j in jsons:
            files.append(j)
        count += 1
    print(f"\n========={count} categories found=========")

    return categories, files


def analyse_json_structure(files):
    """
    Generates a list of all unique key values within the JSONs across all 
    categories.

        :param categories: The directories (categories) as a list.
        :returns: A list of unique keys across all JSON files.
    """
    keys = []
    for file in files:
        with file.open("r", encoding="utf-8") as f:
            data = json.load(f)
            for key, _ in data.items():
                if key not in keys:
                    keys.append(key)
    print(f"\n========={len(keys)} unique keys found=========")

    return keys


def record_instances_of_keys(categories, keys):
    """
    """
    for cat in categories:
        jsons = cat.glob("*.json")
        for j in jsons:
            with j.open("r", encoding="utf-8") as f:
                data = json.load(f)
                filename = f"found_keys_{cat}"
                filename = []
                for key in keys:
                    if key in data and key not in filename:
                        filename.append(key)
        print(f"\nThe keys found in {cat} files are:", filename)
        filename.clear()


def flatten_nested_dictionaries(dictionary, parent_key='', sep='_'):
    """
    """
    items = []
    for k, v in dictionary.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_nested_dictionaries(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            items.append((new_key, ', '.join(map(str, v))))
        else:
            items.append((new_key, v))
            
    return dict(items)


def create_csv(files, out_directory):
    """
    """
    headers = ["field_order","field_type","field_id","label","description",
               "data_source","required","placeholder","options_type",
               "default_value"]
    for file in files:
        keys = []
        output_csv_filename = f"{file.stem}.csv"
        output_csv = out_directory / output_csv_filename
        with file.open("r", encoding="utf-8") as f:
            #read the data
            dictionary = json.load(f)
            #list the keys
            data = flatten_nested_dictionaries(dictionary, parent_key='', sep='_')
            for key, _ in data.items():
                if key not in keys:
                    keys.append(key)
            #open the master csv file
            with open("master_csv_template.csv", mode="r", newline="") as infile:
                reader = csv.reader(infile)
                #open and write the new csv file
                with open(output_csv, mode='w', newline='') as outfile:
                    writer = csv.writer(outfile)
                    data = [row for row in reader if row[1] in keys]                          
                    data.insert(0, headers)  
                    for i in range(1, len(data)):
                        data[i].insert(0, i)          
                    for row in data:
                        writer.writerow(row)


def main():
    """
    Holds the main body of the script.
    """
    a = Path("activity") / "c4mip.json"
    b = Path("frequency") / "1hr.json"
    c = Path("grid_label") / "gm.json"
    d = Path("mip") / "cmip5.json"
    e = Path("model_family") / "cam.json"
    f = Path("organisation") / "cmcc.json"
    g = Path("organisation") / "miroc.json"
    h = Path("resolution") / "1km.json"
    files = [a,b,c,d,e,f,g,h]

    out_directory = Path(".github") / "GEN_ISSUE_TEMPLATE"
    out_directory.mkdir(parents=True, exist_ok=True)

    create_csv(files, out_directory)
    

    for file in files:
        output_python_filename = f"{file.stem}.py"
        output_python = out_directory / output_python_filename
        with open(output_python, "w") as outfile:
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


if __name__ == "__main__":
    main()
