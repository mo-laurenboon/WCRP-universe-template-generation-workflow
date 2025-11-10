
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
    },
    "modifiers": ["new","modify"]
}
