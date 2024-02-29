import json
import mailbox
import re
from email.header import decode_header, make_header
from pathlib import Path

from decouple import config

# Load the personal data and a regex pattern to match URLs with personal tokens. Loaded from .env file to keep the personal data out of the public Finxter GitHub repository.
DATA_DIRECTORY = Path(__file__).parent / "data"
PERSONAL_DATA_NAME = str(config("PERSONAL_DATA_NAME"))
PERSONAL_DATA_ADDRESS = str(config("PERSONAL_DATA_ADDRESS"))
PERSONAL_DATA_COUNTRY_CITY = str(config("PERSONAL_DATA_COUNTRY_CITY"))
PERSONAL_TOKEN_URL_PATTERN = str(config("PERSONAL_TOKEN_URL_PATTERN"))


# Need to decode as the Mbox format makes UTF-8 characters unreadable otherwise
def get_decoded_email_header(header_text):
    # Decode the MIME encoded-word syntax
    decoded_header = decode_header(header_text)
    # Make a header from the decoded header
    header = make_header(decoded_header)
    # Convert the header to a string
    return str(header)


# Replace all personal details and url link tokens in the emails in the mbox file
def replace_personal_details(text):
    new_text = (
        re.sub(PERSONAL_TOKEN_URL_PATTERN, "{Link}", text)
        .replace(PERSONAL_DATA_NAME, "Hey {User}")
        .replace(PERSONAL_DATA_ADDRESS, "{Address}.")
        .replace(PERSONAL_DATA_COUNTRY_CITY, "{City}, {Country}")
        .replace(r"\n\n<p>&nbsp;</p>\n\n<p>&nbsp;</p>", "")
    )
    return new_text


def get_email_body(message):
    if message.is_multipart():
        # Get the plain text version if the email is multipart
        for part in message.get_payload():
            if part.get_content_type() == "text/plain":
                # Replace all personal details and url link tokens in the email
                return replace_personal_details(part.get_payload())
    else:
        # Replace all personal details and url link tokens in the email
        return replace_personal_details(message.get_payload())


# Open the mbox file
mbox = mailbox.mbox(DATA_DIRECTORY / "Finx_dataset.mbox")

data = []

# Iterate over the messages in the mbox file
for message in mbox:
    subject = get_decoded_email_header(message["subject"])
    body = get_email_body(message)
    data.append({"subject": subject, "body": body})

# Save the data to a JSON file
with open(DATA_DIRECTORY / "Finx_dataset.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)
