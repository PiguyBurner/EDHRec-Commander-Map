import re
from unidecode import unidecode

def cleanName(cmdr):
    cmdr = unidecode(cmdr)
    cmdr = re.sub(r'[^a-zA-Z0-9, -]', '', cmdr)
    cmdr = re.sub(" // ", '', cmdr)
    cmdr = re.sub("  ", ' ', cmdr)

    return cmdr 