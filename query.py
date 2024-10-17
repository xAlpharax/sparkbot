#!/usr/bin/env python3

##############################################################################

from dotenv import load_dotenv
import os

load_dotenv()
PREDICTION_API_URL = str(os.getenv("PREDICTION_API_URL"))
JWT = str(os.getenv("JWT"))
HEADERS = { "Authorization": "Bearer " + JWT }

##############################################################################

# import requests

# outdated implementation of the massive time it takes to query the API
# def query(payload):

    # response = requests.post(PREDICTION_API_URL, json=payload).json()
    # print(response)

    # return response

##############################################################################

import aiohttp

async def query(payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(PREDICTION_API_URL, headers=HEADERS, json=payload) as response:
            return await response.json()

##############################################################################

if __name__ == "__main__":

    import asyncio

    async def main():
        output = await query({
            "question": "Hey, what is Photonspark?",
            "chatId": "1234567890",
        })
        return output

    print(asyncio.run(main()))
