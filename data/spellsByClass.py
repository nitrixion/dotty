from model.spell import Spell
from data.spellColors import *

# all classes atm
def getSpellsNecro():
    return {
        #Poison
        "Bane of Nife" : Spell("Bane of Nife", 7, poison()),
        "Envenomed Bolt" : Spell("Envenomed Bolt", 6, poison()),
        #Magic
        "Vexing Mordinia" : Spell("Vexing Mordinia", 9, magic()),
        "Morternum" : Spell("Morternum", 9, magic()),
        "Splurt" : Spell("Splurt", 16, magic()),
        "Soul Well" : Spell("Soul Well", 10, magic()),
        #fire
        "Pyrocruor" : Spell("Pyrocruor", 8, fire()),
        "Ignite Blood" : Spell("Ignite Blood", 7, fire()),
        "Boil Blood" : Spell("Boil Blood", 7, fire()),
        "Heat Blood" : Spell("Heat Blood", 6, fire()),
        #disease
        "Pox of Bertoxxulous" : Spell("Pox of Bertoxxulous", 18, disease()),
        "Plague" : Spell("Plague", 13, disease()),
        "Cessation of Cor" : Spell("Cessation of Cor", 9, disease()),
        #snare
        "Devouring Darkness" : Spell("Devouring Darkness", 13, snare()),
        "Cascading Darkness" : Spell("Cascading Darkness", 16, snare()),
        "Torment of Shadows" : Spell("Torment of Shadows", 16, snare()),
    }