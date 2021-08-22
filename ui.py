#import PySimpleGUI 
# import pandas

from dotty import DotTracker
from logMessages import log
from datetime import datetime
import tkinter as tk
from tkinter.filedialog import askopenfilename

class TextGrid(tk.Canvas):
    def __init__(self, rows, cols, master):
        self.master = master
        tk.Canvas.__init__(self, self.master)
        self.rows = rows
        self.cols = cols
        self.width = 150
        self.height = 30
        
    def create_text_at(self, row, col, text, size):
        """support creation of text at specific positions based on row and column
        """
        x = 25 + self.width * .5 + self.width * (col)
        y = self.height * .5 + self.height * (row)
        self.create_text(x, y, text=text, font="Times "+str(size)+" bold")
    
    def create_rectangle_at(self, row, col, color):
        x = 25 + self.width * (col)
        y = self.height * (row)
        self.create_rectangle(x, y, x + self.width, y + self.height, fill=color)


spellSlots = {}
colors = ['red','blue','green','red','blue','green','red','blue','green','red','blue','green','red','blue','green']

def getRow():
    row = 1
    while row in l:
        row += 1


def updateTable():
    tcv.delete("all")
    col = 0
    row = 0
    for spell in tracker.player.spells:
        if spell in tracker.player.activeSpells:
            row += 1
            spellSlots[spell] = row
            tcv.create_rectangle_at(row, col, tracker.player.spells[spell].color)
            tcv.create_text_at(row, col, spell, 12)

    for npc in tracker.player.activeTargets:
        col += 1
        tcv.create_text_at(0, col, npc, 12)
        for spellName in tracker.player.activeTargets[npc]:
            row = spellSlots[spellName]
            spell = tracker.player.activeTargets[npc][spellName]
            timeLeft = (spell.spell.totalTicks * 6) - (tracker.curTime - spell.startTime).total_seconds()
            if(timeLeft < 10):
                tcv.create_rectangle_at(row, col, '#fe0002')    
            else:
                tcv.create_rectangle_at(row, col, spell.spell.color)
            tcv.create_text_at(row, col,"{0:.0f}s".format(timeLeft), 14)
            #print("*** "+str(row) + " @ " + spellName + " - ticks left: " + str(spell.getRemainingTicks()) + " total: " + str(spell.ticks))

def setWindow():
    w = str((len(tracker.player.activeTargets)+1) * tcv.width + 50)
    h = str((len(tracker.player.activeSpells)+1) * tcv.height + 10)
    root.geometry(w+"x"+h)

def update():
    tracker.nextLine()
    updateTable()
    setWindow()
    root.after(100, update)


# tk().withdraw() # we don't want a full GUI, so keep the root window from appearing


root = tk.Tk()

root.withdraw()
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
log(filename)
root.deiconify()

tcv = TextGrid(12, 4, root)
tracker = DotTracker()
# Skip to the end of the log
tracker.load(filename, True)
log("Loaded")

tcv.pack(expand=True, fill=tk.BOTH)

setWindow()
root.attributes('-topmost', True)
root.configure(bg='black')

root.after(10, update)
root.mainloop()
