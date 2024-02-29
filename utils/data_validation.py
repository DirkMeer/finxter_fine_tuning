import json
from decimal import Decimal
from pathlib import Path

import tiktoken


TRAINING_COST_PER_1000_TOKENS = Decimal("0.0080")


class Validator:
    def __init__(self, jsonl_file: Path) -> None:
        self.data = self._load_data(jsonl_file)
        self._token_list = None
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def _load_data(self, jsonl_file: Path) -> list:
        with open(jsonl_file, "r", encoding="utf-8") as file:
            data = [json.loads(line) for line in file]
        return data

    def _calculate_token_amount_per_entry(self) -> list[int]:
        extra_tokens_per_message = 2
        token_list = []
        for training_data_object in self.data:
            num_tokens = 0
            for message in training_data_object["messages"]:
                for _, value in message.items():
                    num_tokens += len(self.encoding.encode(str(value)))
                    num_tokens += extra_tokens_per_message
            token_list.append(num_tokens)
        return token_list

    def _check_single_entry_format(self, entry) -> bool:
        if not isinstance(entry, dict):
            return False

        if list(entry.keys()) != ["messages"]:
            return False

        messages = entry.get("messages", [])

        return all(
            isinstance(message, dict) and "role" in message and "content" in message
            for message in messages
        )

    @property
    def token_list(self) -> list[int]:
        if self._token_list is None:
            self._token_list = self._calculate_token_amount_per_entry()
        return self._token_list

    def validate_data(self) -> bool:
        return all(self._check_single_entry_format(entry) for entry in self.data)

    def get_training_cost_in_dollars(self, epochs: int = 3) -> Decimal:
        total_tokens = sum(self.token_list)
        total_cost_dollars = (
            TRAINING_COST_PER_1000_TOKENS * total_tokens / 1000 * epochs
        )
        print(
            f"Total estimated cost: ~${total_cost_dollars:.3f} for training {epochs} epochs on {total_tokens} token dataset."
        )
        return total_cost_dollars

    def longest_entry_token_count(self) -> int:
        return max(self.token_list)
