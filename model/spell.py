from data.logMessages import log
import math

class Spell:
    def __init__(self, name, durationTicks, cost, color):
        self.casting = False
        self.name = name
        self.totalTicks = durationTicks
        self.color = color
        self.cost = cost
        self.dpm = 0

    def start(self):
        self.casting = True
        log("Started Casting: " + self.name)


    def interrupt(self):
        self.casting = False
        log("Interrupted: " + self.name)

    def resist(self):
        self.casting = False
        log("Resisted: " + self.name)

    def updateDamagePerMana(self, dpm):
        self.dpm = max(dpm, self.dpm)

class ActiveSpell():
    def __init__(self, spellDef, npc, firstTickAt, mod, timeUntilNextTick):
        self.name = spellDef.name
        self.durationMod = mod
        self.spell = spellDef
        self.totalTicks = self.getSpellTicks()
        self.timeUntilNextTick = timeUntilNextTick
        #self.spell.totalTicks = round(self.spell.totalTicks * mod)
        log("Active spell: " + self.name + " with mod: " + str(mod) + " ticks: " + str(self.totalTicks))
        
        self.ticks = 0
        self.npc = npc
        self.active = True
        self.startTime = firstTickAt
        self.recasting = False
        self.totalDamage = 0
        self.damagePerMana = 0
        self.recastCache = {}
        

    def recast(self):
        log("RECAST: "+ self.name)
        # Bug: issue with instance not being reset. Consider recastStartTime and adding castTime.
        self.recasting = True
        self.recastCache = {"ticks":self.ticks, "time":self.startTime, "used":False, "dpm":self.damagePerMana, "total":self.totalDamage}
    
    def castFailed(self):
        log("RECAST: "+ self.name)
        self.recasting = False
        # Spell was being recast while active and recieved a damage tick after recast started
        # reset values to previous values, destroy cache
        if self.recastCache and self.recastCache["used"]:
            self.ticks = self.recastCache["ticks"]
            self.startTime = self.recastCache["time"]
            # self.damagePerMana = self.recastCache["dpm"]
            # self.totalDamage = self.recastCache["total"]
            self.recastCache = None


    def wornoff(self, npc):
        log("FADE: "+ self.name + " Has finised after ticks: " + str(self.ticks) + " on " + npc)
        self.ticks = 0
        self.active = False
        self.recasting = False

    def end(self, npc):
        log("DIE: "+self.name + " on " + npc + " Has finised after ticks: " + str(self.ticks))
        self.ticks = 0
        self.active = False
        self.recasting = False

    def damage(self, amount, time):
        self.ticks += 1
        self.totalDamage += int(amount)
        self.damagePerMana = self.totalDamage / self.spell.cost
        if(self.ticks <= self.totalTicks):
            self.spell.updateDamagePerMana(self.damagePerMana)

        if(self.recasting):
            log("RESET after recast: " + self.name)
            self.ticks = 1
            self.startTime = time
            self.recasting = False
            self.recastCache["ticks"] += 1
            self.recastCache["used"] = True

        if(self.ticks == 1):
            log(self.name + " started on " + self.npc + " for: " + amount)
        elif self.totalTicks > self.ticks and self.getRemainingTicks() < 3:
            log(self.name + " - fading on " + self.npc + " in " + str((self.totalTicks) * 6) + " seconds.")
        else:
            log(self.name + " tick: " + str(self.ticks) +" on " + self.npc + " for: " + amount)
    
    def getRemainingTicks(self):
        return self.totalTicks - self.ticks

    def getTimeLeft(self, curTime):
        return (self.totalTicks * 6) - (curTime - self.startTime).total_seconds() + self.timeUntilNextTick

    def getSpellTicks(self):
        return round(self.spell.totalTicks * self.durationMod)

