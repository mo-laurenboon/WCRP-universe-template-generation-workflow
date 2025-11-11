
TEMPLATE_CONFIG = {
    "name": "Add/Modify: region",
    "description": "Add or modify region in WCRP Universe",
    "title": "Add/Modify: region: <Type activity name here>",
    "labels": ["region", "cv-submission"]
}

DATA = {
    "issue_types": ["New", "Modify"],
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
    },
    "modifiers": ["new","modify"]
}