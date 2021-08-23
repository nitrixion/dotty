import re

debug = False

logStart = "\[([A-Za-z0-9: ]*)\] "

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
        cache["begin"] = re.compile(logStart + "You begin casting ([A-Za-z ]*).")
    return cache["begin"]

## [Thu Aug 19 19:03:11 2021] An Icepaw kobold warrior has taken 351 damage from your Envenomed Bolt.
# group(0) = whole string
# group(1) = datetime
# group(2) = NPC
# group(3) = damage amount
# group(4) = spell name
def damageRegex():
    if not "damage" in cache:
        cache["damage"] = re.compile(logStart + "([A-Za-z ]*) has taken ([0-9]*) damage from your ([A-Za-z ]*).")
    return cache["damage"]

## [Thu Aug 19 19:58:55 2021] Your Envenomed Bolt spell is interrupted.
# group(0) = whole string
# group(1) = datetime
# group(2) = spell name
def interruptedRegex():
    if not "interrupted" in cache:
        cache["interrupted"] = re.compile(logStart + "Your ([A-Za-z ]*) spell is interrupted.")
    return cache["interrupted"]

## [Thu Aug 19 20:07:54 2021] Icehackle resisted your Envenomed Bolt!
# group(0) = whole string
# group(1) = datetime
# group(2) = NPC
# group(3) = spell name
def resistedRegex():
    if not "resisted" in cache:
        cache["resisted"] = re.compile(logStart + "([A-Za-z ]*) resisted your ([A-Za-z ]*)!")
    return cache["resisted"]


## [Thu Aug 19 21:38:49 2021] King Tormax has been slain by Kenartik!
# group(0) = whole string
# group(1) = datetime
# group(2) = npc
def slainByOtherRegex():
    if not "slainOther" in cache:
        cache["slainOther"] = re.compile(logStart + "([A-Za-z ]*) has been slain")
    return cache["slainOther"]

## [Fri Aug 20 23:45:55 2021] You have slain a large rattlesnake!
# group(0) = whole string
# group(1) = datetime
# group(2) = npc
def slainByYouRegex():
    if not "slainYou" in cache:
        cache["slainYou"] = re.compile(logStart + "You have slain ([A-Za-z ]*)")
    return cache["slainYou"]

## [Thu Aug 19 21:38:49 2021] Your Envenomed Bolt spell has worn off of Velketor the Sorcerer.
# group(0) = whole string
# group(1) = datetime
# group(2) = spell name
# group(3) = npc
def wornoffRegex():
    if not "wornoff" in cache:
        cache["wornoff"] = re.compile(logStart + "Your ([A-Za-z ]*) spell has worn off of ([A-Za-z ]*)")
    return cache["wornoff"]

## [Thu Aug 19 21:38:49 2021] Your Envenomed Bolt spell has worn off of Velketor the Sorcerer.
# group(0) = whole string
# group(1) = datetime
# group(2) = spell name
# group(3) = npc
def overwrittenRegex():
    if not "overwritten" in cache:
        cache["overwritten"] = re.compile(logStart + "Your ([A-Za-z ]*) spell on ([A-Za-z ]*) has been overwritten.")
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