import json
from pathlib import Path
from typing import Iterable


def dicts_to_jsonl(output_file: Path, data: Iterable[dict]) -> Path:
    with open(output_file, "w") as file:
        for dict_obj in data:
            json_string = json.dumps(dict_obj)
            file.write(json_string + "\n")
    return output_file


def json_to_jsonl(input_file: Path, output_file: Path) -> Path:
    with open(input_file, "r") as in_file:
        data = json.load(in_file)

    return dicts_to_jsonl(output_file, data)
