# edhrecMap
 
A fun script I spun up to map all commanders on EDHRec based on simiarity.

## Running

You'll need to `pip install pyedhrec` and `scrython` for MTG specific things, and `networkx` and `plotly` for the graph stuff. I'm lazy and didn't make it a virtual environment.

Then just run `python main.py` (yes you need python for python code, I assume you knew that if you're reading this)

## Settings

### Flags:
`-h` = help
`"-l", "-ls", "--localsource` = use local source (probably not, was for debugging)
`"-a", "-avg", "--avgdeck"` = Use average deck data rather than high synergy cards. I recommmend this.
`"-c", "-conn", "--connectionlimit"` = Threshold for number of required connections. Defaults to 1, and I recommend making at least 15 for average-deck runs. It VERY quickly makes the graph look messy

### Other
I couldn't bother making flags for it, but to change your graph's appearance, mess with `graphCreator.py`'s weightCalc and different layouts. 
WARNING: A lot of the settings take a lot of fiddling about to produce appealing graphs.

## Additional Things
NOTE: This does not include partner cards or partner pairs, as that would nearly double the size and most are not notable.

NOTE: I've uploaded my cached lists of things for your sanity and to save scryfall and EDHRec some server pings. Pulling all that information from their servers takes ~10 minutes because my sleep()s are pretty long to not tax their servers. If you want to adjust the sleeps, don't go shorter than 0.1 (which is what scryfall recommends; there is very little in the ways of EDHRec documentation).

WARNING: Running this thing is very taxing, as it has over 2000 points with many connections for each. My computer can build up a graph in a little over a minute using cached data, but also my computer is quite good.
