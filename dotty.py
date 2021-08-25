import sys
import time
from datetime import datetime
from lineHandler import * 
from data.spellsByClass import getSpellsNecro
from model.player import getPlayer
from data.logMessages import timeRegex
from datetime import datetime
from util import getTime

class DotTracker:
    def __init__(self):
        self.player = getPlayer(getSpellsNecro())
        self.curTime = datetime.time

    def load(self, fileName, toEnd):
        self.file = open(fileName, encoding="utf8")
        if not toEnd:
            return
        while 1:
            line = self.file.readline()
            if not line:
                return

    def nextLine(self):
        while 1:
            line = self.file.readline()
            if not line:
                return
            m = timeRegex().match(line)
            if m:
                self.curTime = getTime(m.group(1))
            m2 = zoningRegex().match(line)
            if m2:
                self.player = getPlayer(getSpellsNecro())
            # Only care about lines with the words Yyou or slain
            if "you" in line or "You" in line or "slain" in line:
                if readLine(line, self.player):
                    return
