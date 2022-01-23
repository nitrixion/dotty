#import PySimpleGUI 
# import pandas

import sys
import tkinter as tk
from datetime import datetime

from dotty import DotTracker
from data.logMessages import log
from tkinter.filedialog import askopenfilename
from tkinter import LEFT, RIGHT, BOTH, RAISED, X
from tkinter.ttk import Frame
# from tkinter.tkSimpleDialog import tkSimpleDialog

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

def getRow():
    row = 1
    while row in l:
        row += 1

def addItemToList(obj, npc, spell):
    if not npc in obj:
        obj[npc] = {}
    if spell:
        obj[npc][spell] = 1

def handleModifier():
    try:
        mod = int(inputtxt.get('1.0', 'end'))
        tracker.updateDurationModifier(mod)
    except ValueError:
        inputtxt.delete("1.0","end")
        inputtxt.insert('end', '0')
    
    #mod = tk.tkSimpleDialog.askstring("Name prompt", "enter your name")

def updateTable():
    tcv.delete("all")
    col = 0
    row = 0
    for spell in tracker.player.spells:
        if spell in tracker.player.activeSpells:
            row += 1
            spellSlots[spell] = row
            s = tracker.player.spells[spell]
            tcv.create_rectangle_at(row, col, s.color)
            if(s.cost > 1):
                tcv.create_text_at(row, col, "{0} ({1:.1f})".format(spell, s.dpm), 12)
            else:
                tcv.create_text_at(row, col, "{0}".format(spell), 12)

    tcv.create_rectangle_at(0, 0, 'white')
    if len(tracker.player.activeTargets) == 0:
        #button = tk.Button(root, text ="Monitoring (Click to add duration modifier)", command = handleModifier)
        #button.pack()
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
            # if(spell.spell.cost > 1):
            #     tcv.create_text_at(row, col,"{0:.0f}s {1:.1f}dpm".format(timeLeft, spell.damagePerMana), 14)
            # else:
            tcv.create_text_at(row, col,"{0:.0f}s".format(timeLeft), 14)

    for npc in cleanup:
        for spell in cleanup[npc]:
            tracker.player.remove(npc,spell)

def setWindow():
    w = str(max((len(tracker.player.activeTargets)+1) * tcv.width + 10, 200))
    h = str((len(tracker.player.activeSpells)+2) * tcv.height + 5)
    root.title("dotty")
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


frame = Frame(root, relief=RAISED, borderwidth=1)
frame.pack(fill=X, expand=True)

button = tk.Button(frame, text ="Set Duration Mod %", command = handleModifier)
#button.place(x=0, y=0)
button.pack(side=LEFT)

inputtxt = tk.Text(frame, height = 1, width = 4)
inputtxt.insert('end', '0')
#inputtxt.place(x=10, y=0)
inputtxt.pack(side=LEFT)

tcv.pack(expand=True, fill=tk.BOTH)

setWindow()
root.attributes('-topmost', True)
root.configure(bg='black')

root.after(10, update)
root.mainloop()
