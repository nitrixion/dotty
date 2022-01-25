import re

debug = True

logStart = "\[([A-Za-z0-9: ]*)\] "

spell = "([A-Za-z ']*)"

npc = "([`A-Za-z \-']*)"

cache = {}

def timeRegex():
    if  not "time" in cache:
        cache["time"] = re.compile(logStart)
    return cache["time"]

## [Thu Aug 19 19:03:07 2021] You begin casting Envenomed Bolt.
# group(0) = whole string
# group(1) = datetime
# group(2) = spell name
def beginCastingRegex():
    if  not "begin" in cache:
        cache["begin"] = re.compile("{0}You begin casting {1}.".format(logStart, spell))
    return cache["begin"]

## [Thu Aug 19 19:03:11 2021] An Icepaw kobold warrior has taken 351 damage from your Envenomed Bolt.
# group(0) = whole string
# group(1) = datetime
# group(2) = NPC
# group(3) = damage amount
# group(4) = spell name
def damageRegex():
    if not "damage" in cache:
        cache["damage"] = re.compile("{0}{1} has taken ([0-9]*) damage from your {2}.".format(logStart, npc, spell))
    return cache["damage"]

## [Thu Aug 19 19:58:55 2021] Your Envenomed Bolt spell is interrupted.
# group(0) = whole string
# group(1) = datetime
# group(2) = spell name
def interruptedRegex():
    if not "interrupted" in cache:
        cache["interrupted"] = re.compile("{0}Your {1} spell is interrupted.".format(logStart, spell))
    return cache["interrupted"]

## [Thu Aug 19 20:07:54 2021] Icehackle resisted your Envenomed Bolt!
# group(0) = whole string
# group(1) = datetime
# group(2) = NPC
# group(3) = spell name
def resistedRegex():
    if not "resisted" in cache:
        cache["resisted"] = re.compile(logStart + "{0}{1} resisted your {2}!".format(logStart, npc, spell))
    return cache["resisted"]


## [Thu Aug 19 21:38:49 2021] King Tormax has been slain by Kenartik!
# group(0) = whole string
# group(1) = datetime
# group(2) = npc
def slainByOtherRegex():
    if not "slainOther" in cache:
        cache["slainOther"] = re.compile("{0}{1} has been slain".format(logStart, npc))
    return cache["slainOther"]

## [Fri Aug 20 23:45:55 2021] You have slain a large rattlesnake!
# group(0) = whole string
# group(1) = datetime
# group(2) = npc
def slainByYouRegex():
    if not "slainYou" in cache:
        cache["slainYou"] = re.compile("{0}You have slain {1}".format(logStart, npc))
    return cache["slainYou"]

## [Thu Aug 19 21:38:49 2021] Your Envenomed Bolt spell has worn off of Velketor the Sorcerer.
# group(0) = whole string
# group(1) = datetime
# group(2) = spell name
# group(3) = npc
def wornoffRegex():
    if not "wornoff" in cache:
        cache["wornoff"] = re.compile("{0}Your {1} spell has worn off of {2}".format(logStart, spell, npc))
    return cache["wornoff"]

## [Thu Aug 19 21:38:49 2021] Your Envenomed Bolt spell has worn off of Velketor the Sorcerer.
# group(0) = whole string
# group(1) = datetime
# group(2) = spell name
# group(3) = npc
def overwrittenRegex():
    if not "overwritten" in cache:
        cache["overwritten"] = re.compile("{0}Your ([A-Za-z ]*) spell on ([`A-Za-z ]*) has been overwritten.".format(logStart, spell, npc))
    return cache["overwritten"]

## [Thu Aug 19 21:38:49 2021] Your Envenomed Bolt spell has worn off of Velketor the Sorcerer.
# group(0) = whole string
# group(1) = datetime
# group(2) = spell name
# group(3) = npc
def zoningRegex():
    if not "zone" in cache:
        cache["zone"] = re.compile(logStart + "LOADING, PLEASE WAIT...")
    return cache["zone"]

def log(text):
    if(debug):
        print(text)