#import PySimpleGUI 
# import pandas

import sys
import tkinter as tk
from datetime import datetime

from dotty import DotTracker
from data.logMessages import log
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
        x = 5 + self.width * .5 + self.width * (col)
        y = self.height * .5 + self.height * (row)
        self.create_text(x, y, text=text, font="Times "+str(size)+" bold")
    
    def create_rectangle_at(self, row, col, color):
        x = 5 + self.width * (col)
        y = self.height * (row)
        self.create_rectangle(x, y, x + self.width, y + self.height, fill=color)


spellSlots = {}
colors = ['red','blue','green','red','blue','green','red','blue','green','red','blue','green','red','blue','green']

def getRow():
    row = 1
    while row in l:
        row += 1

def addItemToList(obj, npc, spell):
    if not npc in obj:
        obj[npc] = {}
    if spell:
        obj[npc][spell] = 1

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

    tcv.create_rectangle_at(0, 0, 'white')
    if len(tracker.player.activeTargets) == 0:
        tcv.create_text_at(0, 0, "Monitoring...", 12)

    cleanup = {}

    for npc in tracker.player.activeTargets:
        col += 1
        tcv.create_rectangle_at(0, col, 'white')
        tcv.create_text_at(0, col, npc, 12)
        # check if we should remove an npc if it has no spells
        if len(tracker.player.activeTargets[npc]) == 0:
            addItemToList(cleanup, npc, None)
        for spellName in tracker.player.activeTargets[npc]:
            spell = tracker.player.activeTargets[npc][spellName]
            if not spell.active:
                # remove non-active spells in case we missed the fade message
                addItemToList(cleanup, npc, spellName)
                continue
            row = spellSlots[spellName]
            timeLeft = spell.getTimeLeft(tracker.curTime)
            if timeLeft < -1:
                # remove spells with neg time, it was either refreshed or faded and we missed the message
                addItemToList(cleanup, npc, spellName)
            elif(timeLeft < 10):
                tcv.create_rectangle_at(row, col, '#fe0002')  
            elif(timeLeft < 18):
                tcv.create_rectangle_at(row, col, '#fffd01')    
            else:
                tcv.create_rectangle_at(row, col, spell.spell.color)
            tcv.create_text_at(row, col,"{0:.0f}s".format(timeLeft), 14)

    if len(cleanup) > 0:
        for npc in cleanup:
            for spell in cleanup[npc]:
                tracker.player.remove(npc,spell)

def setWindow():
    w = str((len(tracker.player.activeTargets)+1) * tcv.width + 10)
    h = str((len(tracker.player.activeSpells)+1) * tcv.height + 5)
    root.geometry(w+"x"+h)

def update():
    tracker.nextLine()
    updateTable()
    setWindow()
    root.after(100, update)

def move(event):
    x, y = root.winfo_pointerxy()
    root.geometry(f"+{x}+{y}")

loadToNow = True
if len(sys.argv) > 1:
    loadToNow = bool(sys.argv[1] == "True")

root = tk.Tk()

root.withdraw()
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
log(filename)
root.deiconify()

tcv = TextGrid(12, 4, root)
tracker = DotTracker()
# Skip to the end of the log
tracker.load(filename, loadToNow)
log("Loaded")

tcv.pack(expand=True, fill=tk.BOTH)

setWindow()
root.attributes('-topmost', True)
root.configure(bg='black')

root.after(10, update)
root.mainloop()
