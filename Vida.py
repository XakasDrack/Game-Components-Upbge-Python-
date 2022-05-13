import bge
from collections import OrderedDict
from bge import logic

cena = bge.logic.getCurrentScene()

def Hp(cont):

    Vida = cena.objects["PHP"]
    #Definir a vida e o limite
    own = cont.owner
    hp = own['PHP']
    own['PHP'] = max (0, min(200, hp))