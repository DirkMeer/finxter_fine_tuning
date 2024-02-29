import json

from tenacity import retry, stop_after_attempt, wait_fixed
from tqdm import tqdm

from constants import CLIENT, DATA_DIRECTORY
from utils import html_email


INPUT_DATA = DATA_DIRECTORY / "Finx_dataset.json"
OUTPUT_DATA = DATA_DIRECTORY / "Finx_completed_dataset.json"
MODEL: str = "gpt-3.5-turbo-0125"
TOTAL_TOKENS_USED = 0
RATE_ERROR_MESSAGE = "There was an error calling 'get_user_query'. Perhaps the OpenAI ChatGPT rate limit has been reached. Retrying one more time in 60 seconds to reset the rate limiter..."


class TrainingDataEntry:
    def __init__(self, fictional_user_query, markdown_email) -> None:
        self.data = {
            "messages": [
                {
                    "role": "system",
                    "content": 'You are a helpful assistant that writes emails for the Finxter email newsletter, adhering perfectly to the style and tone of the Finxter brand and Chris\' writing style. You will respond in the following format: {"subject": "The subject of the email", "body": "The body of the email in Markdown formatting"}.',
                },
                {"role": "user", "content": fictional_user_query},
                {"role": "assistant", "content": markdown_email},
            ]
        }


@retry(
    wait=wait_fixed(60),
    stop=stop_after_attempt(2),
    reraise=True,
    before_sleep=lambda _: print(RATE_ERROR_MESSAGE),
)
def get_fictional_user_query(email: str) -> str:
    global TOTAL_TOKENS_USED
    response = CLIENT.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": 'You will be provided with an email in the following format:{"subject": "The subject of the email", "body": "The body of the email in Markdown formatting"}. Your task is to go back in time and write a rough draft of the topics the email writer decided to discuss in the email. This will basically be a summary of the email\'s topics formatted in short bullet points, that the author would have used as a basis to then write the real email.',
            },
            {
                "role": "user",
                "content": f"Here is the output LLM generated email: {email}. Bullet point draft of the topics discussed in the email:",
            },
        ],
    )
    if not response.usage or not response.choices[0].message.content:
        raise Exception("Invalid response from OpenAI API")
    TOTAL_TOKENS_USED += response.usage.total_tokens
    return response.choices[0].message.content


with open(INPUT_DATA, "r", encoding="utf-8") as file:
    input_data = json.load(file)
    output_data = []
    for finx_email in tqdm(input_data, desc="Generating training data"):
        finx_email["body"] = html_email.html_to_markdown(finx_email["body"])
        training_data_entry = TrainingDataEntry(
            fictional_user_query=get_fictional_user_query(finx_email),
            markdown_email=str(finx_email),
        )
        output_data.append(training_data_entry.data)


with open(OUTPUT_DATA, "w", encoding="utf-8") as file:
    json.dump(output_data, file, indent=4)

print(f"Total tokens used: {TOTAL_TOKENS_USED}")
