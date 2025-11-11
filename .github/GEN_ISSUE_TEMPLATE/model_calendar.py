
TEMPLATE_CONFIG = {
    "name": "Add/Modify: model_calendar",
    "description": "Add or modify model_calendar in WCRP Universe",
    "title": "Add/Modify: model_calendar: <Type activity name here>",
    "labels": ["model_calendar", "cv-submission"]
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