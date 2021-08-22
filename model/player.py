from model.spell import *
from util import getTime

def getPlayer(spells):
    return Player(spells)

class Player:
    def __init__(self, spells):
        self.spells = spells
        self.casting = ""
        self.activeTargets = {}
        self.activeSpells = {}
    
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
    
    def resisted(self, spell):
        if spell in self.spells:
            self.spells[spell].resist()
        self.casting = ""

    def damage(self, spell, amount, npc, time):
        if not spell in self.spells:
            return
        t = getTime(time)
        log(spell + " started damage at " + str(t))
        npc = str.lower(npc)
        if(npc in self.activeTargets):
            if(not spell in self.activeTargets[npc]):
                self.activeTargets[npc][spell] = ActiveSpell(self.spells[spell], npc, t)
                self.activeSpells[spell] = 1
        else: 
            self.activeTargets[npc] = {spell:ActiveSpell(self.spells[spell], npc, t)}
            log("Adding active spell:  " + spell)
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
            if(spell in self.activeSpells):
                self.activeSpells.pop(spell)
            activeSpell = self.activeTargets[npc].pop(spell)
            activeSpell.wornoff(npc)
            if(len(self.activeTargets[npc]) == 0):
                self.activeTargets.pop(npc)
    
    def rebuildActiveSpells(self):
        self.activeSpells.clear()
        for npc in self.activeTargets:
            for spell in self.activeTargets[npc]:
                self.activeSpells[spell] = 1

