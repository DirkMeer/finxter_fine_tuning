import json

from constants import DATA_DIRECTORY
from utils import data_validation, jsonl


JSON_FILE = DATA_DIRECTORY / "Finx_completed_dataset.json"
JSONL_FILE = DATA_DIRECTORY / "Finx_completed_dataset.jsonl"
LIMIT = None


with open(JSON_FILE, "r", encoding="utf-8") as in_file:
    data = json.load(in_file)
    jsonl.dicts_to_jsonl(JSONL_FILE, data[:LIMIT])

data_validator = data_validation.Validator(JSONL_FILE)

print(f"Data valid: {data_validator.validate_data()}")
data_validator.get_training_cost_in_dollars()
print(f"Longest entry: {data_validator.longest_entry_token_count()} tokens")
