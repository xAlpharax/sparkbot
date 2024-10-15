##############################################################################

from dotenv import load_dotenv
import os

load_dotenv()
UPSERT_API_URL = str(os.getenv("UPSERT_API_URL"))
JWT = str(os.getenv("JWT"))
HEADERS = { "Authorization": "Bearer " + JWT }

##############################################################################

import requests

def upsert(payload):

    response = requests.post(UPSERT_API_URL, headers=HEADERS, json=payload).json()

    return response

##############################################################################

# output = upsert({
    # "overrideConfig": {
        # "topK": 1,
        # "baseUrl": "example",
        # "modelName": "example",
        # "numGpu": 1,
    # }
# })

if __name__ == "__main__":
    output = upsert({})
    print(output)
