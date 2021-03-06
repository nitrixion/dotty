from model.spell import *
from util import getTime
import datetime

def getPlayer(spells):
    return Player(spells)

class Player:
    def __init__(self, spells):
        self.spells = spells
        self.casting = ""
        self.activeTargets = {}
        self.activeSpells = {}
        self.durationMod = 1
        self.lastTick = 0
    
    def get_casting(self):
        return self.casting

    def startCasting(self, spell):
        self.casting = spell
        if spell in self.spells:
            self.spells[spell].start()
        if(len(self.activeTargets) == 1):
            target = list(self.activeTargets.values())[0]
            if(spell in target):
                target[spell].recast()

    def interrupted(self, spell):
        if spell in self.spells:
            self.spells[spell].interrupt()
        self.casting = ""
        if(len(self.activeTargets) == 1):
            target = list(self.activeTargets.values())[0]
            if(spell in target):
                target[spell].castFailed()
    
    def resisted(self, spell):
        if spell in self.spells:
            self.spells[spell].resist()
        self.casting = ""
        if(len(self.activeTargets) == 1):
            target = list(self.activeTargets.values())[0]
            if(spell in target):
                target[spell].castFailed()

    def damage(self, spell, amount, npc, time):
        if not spell in self.spells:
            return
        t = getTime(time)
        log(spell + " started damage at " + str(t))
        npc = str.lower(npc)
        self.lastTick = t
        if(npc in self.activeTargets):
            if(not spell in self.activeTargets[npc]):
                self.activeTargets[npc][spell] = ActiveSpell(self.spells[spell], npc, t, self.durationMod, self.timeUntilNextTick(t))
                self.activeSpells[spell] = 1
        else: 
            self.activeTargets[npc] = {spell:ActiveSpell(self.spells[spell], npc, t, self.durationMod, self.timeUntilNextTick(t))}
            self.activeSpells[spell] = 1
        self.activeTargets[npc][spell].damage(amount, t)

    def npcKilled(self, npc):
        npc = str.lower(npc)
        if npc in self.activeTargets:
            target = self.activeTargets.pop(npc)
            for spell in target:
                target[spell].end(npc)
            self.rebuildActiveSpells()
            
     
    def spellWornoff(self, spell, npc):
        npc = str.lower(npc)
        if npc in self.activeTargets and spell in self.activeTargets[npc]:
            activeSpell = self.activeTargets[npc].pop(spell)
            activeSpell.wornoff(npc)
            if(len(self.activeTargets[npc]) == 0):
                self.activeTargets.pop(npc)
            self.rebuildActiveSpells()
    
    def remove(self, npc, spell):
        if npc in self.activeTargets:
            if spell in self.activeTargets[npc]:
                self.activeTargets[npc].pop(spell)
            if len(self.activeTargets[npc]) == 0:
                self.activeTargets.pop(npc)
        self.rebuildActiveSpells()

    def rebuildActiveSpells(self):
        self.activeSpells.clear()
        for npc in self.activeTargets:
            for spell in self.activeTargets[npc]:
                if(self.activeTargets[npc][spell].active):
                    self.activeSpells[spell] = 1

    def durationModifier(self, mod):
        self.durationMod = 1.0 + mod / 100.0

    def timeUntilNextTick(self, curTime):
        if self.lastTick == 0:
            return 0
        nextTick = self.lastTick + datetime.timedelta(seconds=6)
        seconds = (nextTick - curTime).total_seconds()
        if seconds > 0:
            return seconds
        return 0

            

