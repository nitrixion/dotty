from data.logMessages import log
class Spell:
    def __init__(self, name, durationTicks, color):
        self.casting = False
        self.name = name
        self.totalTicks = durationTicks
        self.color = color

    def start(self):
        self.casting = True
        log("Started Casting: " + self.name)


    def interrupt(self):
        self.casting = False
        log("Interrupted: " + self.name)

    def resist(self):
        self.casting = False
        log("Resisted: " + self.name)

class ActiveSpell():
    def __init__(self, spellDef, npc, firstTickAt):
        self.name = spellDef.name
        self.spell = spellDef
        self.ticks = 0
        self.npc = npc
        self.active = True
        self.startTime = firstTickAt
        self.recasting = False

    def recast(self):
        log("RECAST: "+ self.name)
        self.recasting = True
        self.recastCache = {"ticks":self.ticks, "time":self.startTime, "used":False}
    
    def castFailed(self):
        log("RECAST: "+ self.name)
        self.recasting = False
        # Spell was being recast while active and recieved a damage tick after recast started
        # reset values to previous values, destroy cache
        if self.recastCache and self.recastCache["used"]:
            self.ticks = self.recastCache["ticks"]
            self.startTime = self.recastCache["time"]
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
        if(self.recasting):
            log("RESET after recast: " + self.name)
            self.ticks = 0
            self.startTime = time
            self.recasting = False
            self.recastCache["ticks"] += 1
            self.recastCache["used"] = True
        self.ticks += 1
        
        if(self.ticks == 1):
            log(self.name + " started on " + self.npc + " for: " + amount)
        elif self.spell.totalTicks > self.ticks and self.spell.totalTicks - self.ticks < 3:
            log(self.name + " - fading on " + self.npc + " in " + str((self.spell.totalTicks - self.ticks) * 6) + " seconds.")
        else:
            log(self.name + " tick: " + str(self.ticks) +" on " + self.npc + " for: " + amount)
    
    def getRemainingTicks(self):
        return self.spell.totalTicks - self.ticks


