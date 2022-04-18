
def poison():#green
    return '#71aa34'
def magic(): #blue
    return '#c3fbf4'
def fire(): #pink
    return '#fdb0c0'
def disease(): #light brown
    return '#c9ae74'
def snare():# light urple
    return '#ceaefa'


def getColor(spellType):
    match spellType:
        case "poison":
            return poison()
        case "disease":
            return disease()
        case "fire":
            return fire()
        case "magic":
            return magic()
        case "snare":
            return snare()