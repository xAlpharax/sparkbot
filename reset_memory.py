#!/usr/bin/env python3

##############################################################################

from dotenv import load_dotenv
import os

load_dotenv()

RESET_MEMORY_API_URL = str(os.getenv("RESET_MEMORY_API_URL"))
JWT = str(os.getenv("JWT"))
HEADERS = { "Authorization": "Bearer " + JWT }

##############################################################################

import requests

# as per https://docs.flowiseai.com/api-reference/chat-message
def reset_memory():

    response = requests.delete(
        RESET_MEMORY_API_URL,
        headers=HEADERS,
    ).json()

    return response

##############################################################################

if __name__ == "__main__":
    response = reset_memory()  # Call the reset function

    if response.get("error"):
        print("Reset failed. Please check the error messages above.")
    else:
        print("Reset successful:", response)
