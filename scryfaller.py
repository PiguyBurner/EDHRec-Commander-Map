import scrython as scrython
import scrython.cards

import os
import time
import json 

import utils

COMMANDERS_CACHE_FILE = "cache/commander_list.json"

def getCommanders():
    cmdr_names = []

    page = 1
    while True:
        response = scrython.cards.Search(q="is:commander format=commander -is:partner", order="edhrec", page=page)
        cmdr_names.extend(utils.cleanName(card["name"]) for card in response.data())

        if not response.has_more():
            break

        page += 1
        time.sleep(0.2)

    return cmdr_names

def cacheCommanders():
    if os.path.exists(COMMANDERS_CACHE_FILE):  # Check if the cache exists
        print("Using cached commander list")
        with open(COMMANDERS_CACHE_FILE, "r") as file:
            return json.load(file)  # Load cached data

    # Fetch and save if no cache is found
    commanders = getCommanders()
    with open(COMMANDERS_CACHE_FILE, "w") as file:
        json.dump(commanders, file)  # Save data to cache

    return commanders