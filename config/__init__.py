import json

from utils import resource_path


SETTINGS_PATH = resource_path(

    "config/settings.json"
)

with open(

    SETTINGS_PATH,
    "r",
    encoding="utf-8"

) as f:

    SETTINGS = json.load(f)