import bge
from collections import OrderedDict

keyboard = bge.logic.keyboard.inputs
keyTAP = bge.logic.KX_INPUT_JUST_ACTIVATED
mouse = bge.logic.mouse.inputs


def up_stamina(cont):
    own = cont.owner
#W
    if keyboard[bge.events.LEFTSHIFTKEY].active and keyboard[bge.events.WKEY].active:
        s = own['PropStamina']
        s -= 7
        own['PropStamina'] = max(0, min(300, s))

#A
    elif keyboard[bge.events.LEFTSHIFTKEY].active and keyboard[bge.events.AKEY].active:
        s = own['PropStamina']
        s -= 7
        own['PropStamina'] = max(0, min(300, s))

#S
    elif keyboard[bge.events.LEFTSHIFTKEY].active and keyboard[bge.events.SKEY].active:
        s = own['PropStamina']
        s -= 7
        own['PropStamina'] = max(0, min(300, s))

#D
    elif keyboard[bge.events.LEFTSHIFTKEY].active and keyboard[bge.events.DKEY].active:
        s = own['PropStamina']
        s -= 7
        own['PropStamina'] = max(0, min(300, s))

    else:
        own = cont.owner
        s = own['PropStamina']
        s += 4
        own['PropStamina'] = max(0, min(300, s))