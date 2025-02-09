import helpers.textToList as txtHelper
import scryfaller
import edhreccer
import graphCreator

import argparse

# Connection limit of 10 is the bare minimum for average deck, with 25-30 being reasonable
# 40+ is a pretty strong association

parser = argparse.ArgumentParser()
parser.add_argument("-l", "-ls", "--localsource", help="use local commander list?", action='store_true')
parser.add_argument("-a", "-avg", "--avgdeck", help="use average deck over synergy", action='store_true')
parser.add_argument("-c", "-conn", "--connectionlimit", help="Draws connections if N cards are shared", type=int, default=1)

args = parser.parse_args()

def main():
    if (args.avgdeck):    
        print("Using average deck")
    else:
        print("using high synergy cards")

    # get all possible commanders
    cmdr_list = []

    print("Getting commanders...")

    if (args.localsource):    
        print("Local list selected!")
        cmdr_list = txtHelper.createListFromText()
    else:
        cmdr_list = scryfaller.cacheCommanders()

    print("Getting EDHRec data...")
    synergy_map = edhreccer.cacheSynergy(cmdr_list, localsource=args.localsource, avgDeck=args.avgdeck)

    # a little sanity check because if the limit is 1, then everything will connect up
    if args.avgdeck and args.connectionlimit == 1:
        args.connectionlimit = 10

    graphCreator.createGraph(synergy_map, args.connectionlimit)




if __name__ == '__main__':
    main()