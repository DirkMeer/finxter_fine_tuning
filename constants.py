from pathlib import Path

from decouple import config
from openai import OpenAI


CLIENT = OpenAI(api_key=str(config("OPENAI_API_KEY")))
DATA_DIRECTORY = Path(__file__).parent / "data"
OUTPUT_DIRECTORY = Path(__file__).parent / "output"
CHRIS_GPT = "ft:gpt-3.5-turbo-1106:personal:chris-gpt-full:8ot8ZLJR"
