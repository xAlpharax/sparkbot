import requests

API_URL = "***REMOVED***"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

output = query({
    "question": "Hey, what is Photonspark?",
})

print(output)
