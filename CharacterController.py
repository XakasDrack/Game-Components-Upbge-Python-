import bpy,bge,time
from collections import OrderedDict
from mathutils import Vector, Matrix
import Vida
import joystick
import Stamina

#status // pegando os Status da interface
#sceneList = bge.logic.getSceneList()
#CenaInterface = sceneList[1]
#ObjetosInterface = CenaInterface.objects
cena = bge.logic.getCurrentScene()


#atividades
LimiteStaminaCorrida = 20
LimiteStaminaPulo = 39
Pulo = False
VelEsquiva = 30
podeControlar = True
podeTomarDano = True
PLAYER_DETECTION_RANGE = 10.0
PLAYER_ATTACK_RANGE = 2.25


def clamp(x, a, b):
	return min(max(a, x), b)

class CharacterController(bge.types.KX_PythonComponent):

	args = OrderedDict([
		("Activate", True),
		("Walk Speed", 0.1),
		("Run Speed", 0.2),
		("PHP", 200),
		("PStamina", 300),
		("Max Jumps", 1),
		("Avoid Sliding", True),
		("Static Jump Direction", False),
		("Static Jump Rotation", False),
		("Smooth Character Movement", 0.0),
		("Make Object Invisible", False),
	])

	def start(self, args):

		self.active = args["Activate"]

		self.arm = self.object.children.get("Armature")

		#Status jogador
		self.Status = cena.objects["Jogador"]
		self.Vida = self.Status["PHP"]
		self.Stamina = self.Status["PStamina"]

		self.walkSpeed = args["Walk Speed"]
		self.runSpeed = args["Run Speed"]

		self.avoidSliding = args["Avoid Sliding"]
		self.__lastPosition = self.object.worldPosition.copy()
		self.__lastDirection = Vector([0,0,0])
		self.__smoothSlidingFlag = False

		self.__smoothMov = clamp(args["Smooth Character Movement"], 0, 0.99)
		self.__smoothLast = Vector([0,0,0])

		self.staticJump = args["Static Jump Direction"]
		self.__jumpDirection = [0,0,0]

		self.staticJumpRot = args["Static Jump Rotation"]
		self.__jumpRotation = Matrix.Identity(3)

		self.character = bge.constraints.getCharacter(self.object)
		self.character.maxJumps = args["Max Jumps"]

		if self.active:
			if args["Make Object Invisible"]:
				self.object.visible = False

	def Status(self):

		Vida = cena.objects["Jogador"]

		# Definir a vida e o limite
		Vida["PHP"] = max(0, min(200, Vida))

		if Vida['PHP'] < 1:
			podeControlar = False



#Movimento,Pulo,Esquiva junto com o Sistema de Gasto da Stamina
	def characterMovement(self):

		keyboard = bge.logic.keyboard.inputs
		KeyTAP = bge.logic.KX_INPUT_JUST_ACTIVATED
		Stamina = cena.objects["Jogador"]

		x = 0
		y = 0
		speed = self.walkSpeed

		if podeControlar:
			if self.walkSpeed:
				#self.arm.playAction("Run", 1, 17,blendin = 6)
				if keyboard[bge.events.LEFTSHIFTKEY].active:
					speed = self.runSpeed
				#Sistema da Stamina (quando acabar,nao pode correr nem pular)
					#Gasto de Stamina na corrida no Script "Stamina.py"
					#nao pode correr
					if Stamina["PStamina"] <= LimiteStaminaCorrida:
						speed = self.walkSpeed

				#nao pode pular
				if Stamina["PStamina"] <= LimiteStaminaPulo:
					self.character.maxJumps = 0

				else:
					self.character.maxJumps = 1


				#Movimento WASD nos eixos X e Y
				if keyboard[bge.events.WKEY].active:   y = 1
				elif keyboard[bge.events.SKEY].active: y = -1
				if keyboard[bge.events.AKEY].active:   x = -1
				elif keyboard[bge.events.DKEY].active: x = 1
				#if KeyTAP in keyboard[bge.events.SPACEKEY].queue: y = -5


				#Anula o movimento se teclas diferentes,do mesmo eixo, forem acionadas
				if keyboard[bge.events.WKEY].active and keyboard[bge.events.SKEY].active: y = 0
				if keyboard[bge.events.AKEY].active and keyboard[bge.events.DKEY].active: x = 0

				vec = Vector([x, y, 0])
				self.__smoothSlidingFlag = False

				if vec.length != 0:
					self.__smoothSlidingFlag = True

					vec.normalize()

					vec *= speed
				#Checagem se o personagem esta no chao,e correção da direção do pulo
				if not self.character.onGround:
					self.character.maxJumps = 0
					if self.staticJump:
						vec = self.__jumpDirection
					if self.staticJumpRot:
						self.object.worldOrientation = self.__jumpRotation.copy()
				else:#elif self.character.onGround:
					self.__jumpDirection = vec
					self.__jumpRotation  = self.object.worldOrientation.copy()



				smooth = 1.0 - self.__smoothMov
				vec = self.__smoothLast.lerp(vec, smooth)
				self.__smoothLast = vec
				test = self.object.worldPosition.copy()
				self.character.walkDirection = self.object.worldOrientation @ vec


				if vec.length != 0:
					self.__lastDirection = self.object.worldPosition - self.__lastPosition
					self.__lastPosition = self.object.worldPosition.copy()


	def characterJump(self):
		#pulo

		keyboard = bge.logic.keyboard.inputs
		keyTAP = bge.logic.KX_INPUT_JUST_ACTIVATED
		if podeControlar:
			#Pulo
			if self.walkSpeed:
				Pulo = True
				if Pulo == True:
					if keyboard[bge.events.LEFTSHIFTKEY].active and keyTAP in keyboard[bge.events.SPACEKEY].queue:
						self.character.jump()


	#
	def avoidSlide(self):
		#Correção do bug de ficar deslizando

		self.object.worldPosition.xy = self.__lastPosition.xy

		other = self.object.worldOrientation @ self.__smoothLast

		if self.__lastDirection.length != 0 and other.length != 0:
			if self.__lastDirection.angle(other) > 0.5:
				if not self.__smoothSlidingFlag:
					self.__smoothLast = Vector([0,0,0])

	def update(self):
		if self.active:
			self.characterMovement()
			self.characterJump()
			self.Status()

			if self.avoidSliding:
				self.avoidSlide()

