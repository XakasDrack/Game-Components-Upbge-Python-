import bge
from collections import OrderedDict
from bge import logic



def Stamina(cont):
    own = cont.owner
    keyboard = bge.logic.keyboard.inputs

    # W
    if keyboard[bge.events.LEFTSHIFTKEY].active and keyboard[bge.events.WKEY].active:
        s = own['PStamina']
        s -= 7
        own['PStamina'] = max(0, min(300, s))

    # A
    elif keyboard[bge.events.LEFTSHIFTKEY].active and keyboard[bge.events.AKEY].active:
        s = own['PStamina']
        s -= 7
        own['PStamina'] = max(0, min(300, s))

    # S
    elif keyboard[bge.events.LEFTSHIFTKEY].active and keyboard[bge.events.SKEY].active:
        s = own['PStamina']
        s -= 7
        own['PStamina'] = max(0, min(300, s))

    # D
    elif keyboard[bge.events.LEFTSHIFTKEY].active and keyboard[bge.events.DKEY].active:
        s = own['PStamina']
        s -= 7
        own['PStamina'] = max(0, min(300, s))

    #Recuperação de Stamina
    else:
        own = cont.owner
        s = own['PStamina']
        s += 4
        own['PStamina'] = max(0, min(300, s))