import requests

API_URL = "***REMOVED***"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

if __name__ == "__main__":

    output = query({
        "question": "Hey, what is Photonspark?",
    })

    print(output)
