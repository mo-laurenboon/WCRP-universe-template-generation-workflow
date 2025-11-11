
TEMPLATE_CONFIG = {
    "name": "Add/Modify: native_vertical_grid_coordinate",
    "description": "Add or modify native_vertical_grid_coordinate in WCRP Universe",
    "title": "Add/Modify: native_vertical_grid_coordinate: <Type activity name here>",
    "labels": ["native_vertical_grid_coordinate", "cv-submission"]
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