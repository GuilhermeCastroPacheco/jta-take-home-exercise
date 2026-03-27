import json
import os

def get_universities() -> dict:
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'universities.json')
    with open(path, 'r') as f:
        return json.load(f)