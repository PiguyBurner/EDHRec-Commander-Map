import os
import time
import json 

from pyedhrec import EDHRec

SYNERGY_CACHE_FILE = 'cache/synergy_list.json'
SYNERGY_CACHE_FILE_FOR_LOCAL = 'cache/synergy_list_local.json'

AVG_DECK_CACHE_FILE = 'cache/avg_deck_list.json'
AVG_DECK_CACHE_FILE_FOR_LOCAL = 'cache/avg_deck_list_local.json'


# TODO DFCs and partners are handled the same way on EDHRec, so we want some way to distinguish them
def getEdhrec(cmdr_list, func):
    edhrec = EDHRec()

    synergy_list = {}
    for i in range(len(cmdr_list)):
        if i % 25 == 0:
            print("EDHRec data: {0} / {1} complete".format(i, len(cmdr_list)))
        cmdr = cmdr_list[i]
        try:
            response = func(edhrec, synergy_list, cmdr)
        except: # some cards like partners and backgrounds make it mad
            print("could not get {0}".format(cmdr))
        finally:
            time.sleep(0.2)
    
    return synergy_list


def cacheSynergy(cmdr_list, localsource=False, avgDeck=False):
    if avgDeck:
        cacheFile = AVG_DECK_CACHE_FILE_FOR_LOCAL if localsource else AVG_DECK_CACHE_FILE
    else:
        cacheFile = SYNERGY_CACHE_FILE_FOR_LOCAL if localsource else SYNERGY_CACHE_FILE

    if os.path.exists(cacheFile):  # Check if the cache exists
        print("Using cached file {0}".format(cacheFile))
        with open(cacheFile, "r") as file:
            return json.load(file)  # Load cached data

    # Fetch and save if no cache is found
    synergyCards = []
    if avgDeck:
        synergyCards = getEdhrec(cmdr_list, getAvgDeck)
    else:
        synergyCards = getEdhrec(cmdr_list, getHighSynergy)
    with open(cacheFile, "w") as file:
        json.dump(synergyCards, file)  # Save data to cache

    return synergyCards


def getHighSynergy(edhrec, ls, cmdr):
    try:
        response = edhrec.get_high_synergy_cards(cmdr)['High Synergy Cards']
        ls[cmdr] = [card['name'] for card in response]

    except:
        print("{1} failed!".format(cmdr))
    
    finally:
        return ls
    
def getAvgDeck(edhrec, ls, cmdr):
    try:
        response = edhrec.get_commanders_average_deck(cmdr)['decklist']
        ls[cmdr] = response

    except:
        print("{1} failed!".format(cmdr))
    finally:
        return ls