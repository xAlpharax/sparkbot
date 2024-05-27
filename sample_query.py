##############################################################################

from dotenv import load_dotenv
import os

load_dotenv()
API_URL = str(os.getenv("API_URL"))

import requests

def query(payload):

    response = requests.post(API_URL, json=payload).json()
    print(response)

    return response

##############################################################################

if __name__ == "__main__":
    output = query({
        "question": "Hey, what is Photonspark?",
    })
