from data.logMessages import *

def readLine(text, player):
    matchfound = False
    m = beginCastingRegex().match(text)
    if m:
        player.startCasting(m.group(2))
        matchfound = True

    if not matchfound and len(player.casting) > 0:
        m1 = interruptedRegex().match(text)
        if m1:
            player.interrupted(m1.group(2))
            matchfound = True
        else:
            m2 = resistedRegex().match(text)
            if m2:
                player.resisted(m2.group(3))
                matchfound = True

    if not matchfound:
        m3 = damageRegex().match(text)
        if m3:
            player.damage(m3.group(4), m3.group(3), m3.group(2), m3.group(1))
            matchfound = True
    
    if not matchfound:
        m4 = slainByOtherRegex().match(text)
        if m4:
            player.npcKilled(m4.group(2))
            matchfound = True

    if not matchfound:
        m6 = slainByYouRegex().match(text)
        if m6:
            log("Killed by you - " + m6.group(2))
            player.npcKilled(m6.group(2))
            matchfound = True
    
    if not matchfound:
        m5 = wornoffRegex().match(text)
        if m5:
            player.spellWornoff(m5.group(2), m5.group(3))
            matchfound = True
            
    if not matchfound:
        m6 = overwrittenRegex().match(text)
        if m6:
            player.spellWornoff(m6.group(2), m6.group(3))
            matchfound = True
    return matchfound
    