from model.spell import Spell
from data.spellColors import *

# all classes atm
def getSpellsNecro():
    return {
        #Poison
        "Bane of Nife" : Spell("Bane of Nife", 7, 860, poison()),
        "Envenomed Bolt" : Spell("Envenomed Bolt", 6, 409, poison()),
        #Magic
        "Vexing Mordinia" : Spell("Vexing Mordinia", 9, 495, magic()),
        "Morternum" : Spell("Morternum", 9, 1, magic()),
        "Splurt" : Spell("Splurt", 16, 237, magic()),
        "Soul Well" : Spell("Soul Well", 10, 1, magic()),
        #fire
        "Pyrocruor" : Spell("Pyrocruor", 8, 295,fire()),
        "Ignite Blood" : Spell("Ignite Blood", 7, 218, fire()),
        "Boil Blood" : Spell("Boil Blood", 7, 136, fire()),
        "Heat Blood" : Spell("Heat Blood", 6, 88, fire()),
        #disease
        "Pox of Bertoxxulous" : Spell("Pox of Bertoxxulous", 18, 579, disease()),
        "Plague" : Spell("Plague", 13, 308, disease()),
        "Cessation of Cor" : Spell("Cessation of Cor", 9, 203, disease()),
        #snare
        "Devouring Darkness" : Spell("Devouring Darkness", 13, 400, snare()),
        "Cascading Darkness" : Spell("Cascading Darkness", 16, 300, snare()),
        "Torment of Shadows" : Spell("Torment of Shadows", 16, 1, snare()),
        #druid
        "Winged Death" : Spell("Winged Death", 9, 468, magic()),
        "Wrath of Nature" : Spell("Wrath of Nature", 30, 1, magic()),
        "Drones of Doom" : Spell("Drones of Doom", 8, 287, magic()),
    }