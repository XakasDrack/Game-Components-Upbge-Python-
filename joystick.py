import bge
from mathutils import Vector

def getJoystickButtons(self):
    frame = bge.logic.getAverageFrameRate()/100
    
    b_just = bge.logic.KX_INPUT_JUST_ACTIVATED
    b_active = bge.logic.KX_INPUT_ACTIVE
    b_release = bge.logic.KX_INPUT_JUST_RELEASED
    
    joy = self.object.sensors['Buttons']
    
    buttons = [
        joy.getButtonStatus(0),
        joy.getButtonStatus(1),
        joy.getButtonStatus(2),
        joy.getButtonStatus(3),
        joy.getButtonStatus(4),
        joy.getButtonStatus(6),
        joy.getButtonStatus(7),
        joy.getButtonStatus(8),
        joy.getButtonStatus(9),
        joy.getButtonStatus(10),
        joy.getButtonStatus(11),
        joy.getButtonStatus(12),
        joy.getButtonStatus(13),
        joy.getButtonStatus(14)
    ]
        
    if not "init" in self:
        self['Pressed'] = 0
        self['active'] = 0
        self['released'] = 0
    
    for act in buttons:
        if act == True:
            self['Pressed'] = buttons.index(act)
            self['active'] = buttons.index(act)
            self['released'] = buttons.index(act)
            
    if joy.status == b_just:
        pass
    else:
        self['Pressed'] = -1
    if joy.status == b_active:
        pass
    else:
        self['active'] = -1
    if joy.status == b_release:
        pass
    else:
        self['released'] = -1
        
    return (self['Pressed'], self['active'], self['released'])

def getJoystickAxis(self):
    frame = bge.logic.getAverageFrameRate()/100
    
    axi = self.object.sensors['Buttons']
    
    def axis_set():
        axis_limit = 4000
        axis_divisor = 100000
        axis_one = 32767
        axis = axi.axisValues

        if abs(axis[0]) < axis_limit:
            axis[0] = 0.0
        if abs(axis[1]) < axis_limit:
            axis[1] = 0.0
        if abs(axis[2]) < axis_limit:
            axis[2] = 0.0
        if abs(axis[3]) < axis_limit:
            axis[3] = 0.0
        
        def reducer():
            left_x_reducer = round(((axis[0]/axis_divisor)*(axis[0]/327670)*30.52), 4)
            left_y_reducer = round(((axis[1]/axis_divisor)*(axis[1]/327670)*30.52), 4)
            right_x_reducer = round(((axis[2]/axis_divisor)*(axis[2]/327670)*30.52), 4)
            right_y_reducer = round(((axis[3]/axis_divisor)*(axis[3]/327670)*30.52), 4)
            left_T_reducer = round(((axis[4]/axis_divisor)*(axis[4]/327670)*30.52), 4)
            right_T_reducer = round(((axis[5]/axis_divisor)*(axis[5]/327670)*30.52), 4)
            
            left_x = round((axis[0]*left_x_reducer)/axis_one, 4)
            left_y = round((axis[1]*left_y_reducer)/axis_one, 4)
            right_x = round((axis[2]*right_x_reducer)/axis_one, 4)
            right_y = round((axis[3]*right_y_reducer)/axis_one, 4)
            left_T = round((axis[4]*left_T_reducer)/axis_one, 4)
            right_T = round((axis[5]*right_T_reducer)/axis_one, 4)
            
            axis_vect = Vector((left_x,
                left_y,
                right_x,
                right_y,
                left_T,
                right_T
            ))

            return axis_vect
        return reducer()
    return axis_set()
	
def getConectionStatus(self):
	status = self.object.sensors['Buttons'].connected
	return status
