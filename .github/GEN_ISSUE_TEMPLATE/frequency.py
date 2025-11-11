
TEMPLATE_CONFIG = {
    "name": "Add/Modify: frequency",
    "description": "Add or modify frequency in WCRP Universe",
    "title": "Add/Modify: frequency: <Type activity name here>",
    "labels": ["frequency", "cv-submission"]
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
}