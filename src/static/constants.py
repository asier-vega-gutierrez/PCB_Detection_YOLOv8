
"""Clase con todas las constantes"""
class Constants:
    
    def __init__(self) -> None:

        #Constantes de pcbs
        self.ARDUINO_MEGA = 0
        self.ESP32 = 1
        self.L298N = 2
        self.ULN2003 = 3

        #Nuemro de componente de cada pcb
        self.ARDUINO_MEGA_COUNT = 59
        self.ESP32_COUNT = 27
        self.L298N_COUNT = 21
        self.ULN2003_COUNT = 13
        
        #Constantes de componentes
        self.IC = 0 #
        self.LED = 1 #
        self.BATTERY = 2 #
        self.BUZZER = 3 #
        self.CAPACITOR = 4 
        self.CLOCK = 5
        self.CONNECTOR = 6
        self.DIODE = 7
        self.DISPLAY = 8
        self.FUSE = 9
        self.INDUCTOR = 10
        self.POTENTIOMETER = 11
        self.RELAY = 12
        self.RESISTOR = 13
        self.SWITCH = 14
        self.TRANSISTOR = 15

        #Constantes de componentes por pcb
        self.ARDUINO_MEGA_COMPONENTS = {self.SWITCH: 1, self.CAPACITOR: 14, self.CLOCK: 2, self.CONNECTOR: 12, self.DIODE: 2, self.FUSE: 1, self.IC: 7, self.LED: 4, self.RESISTOR: 11}
        self.ESP32_COMPONENTS = {self.RESISTOR: 10, self.IC: 6, self.LED: 1, self.CAPACITOR: 7, self.CONNECTOR: 3, self.DIODE: 1}
        self.L298N = {self.IC: 2, self.LED: 1, self.CAPACITOR: 2, self.RESISTOR: 1, self.DIODE: 8, self.CONNECTOR: 7}
        self.ULN2003 = {self.IC: 1, self.CONNECTOR: 3, self.RESISTOR: 4, self.LED: 4, self.CAPACITOR: 1}

    """Metodo para cabiar de id a string"""
    def id_to_name(self, id, component):
        if component == False:
            if id == 0:
                return 'ARDUINO_MEGA'
            elif id == 1:
                return 'ESP32'
            elif id == 2:
                return 'L298N'
            elif id == 3:
                return 'ULN2003'
            else:
                return None
        else:
            if id == 0:
                return 'IC'
            elif id == 1:
                return 'LED'
            elif id == 2:
                return 'BATTERY'
            elif id == 3:
                return 'BUZZER'
            elif id == 4:
                return 'CAPACITOR'
            elif id == 5:
                return 'CLOCK'
            elif id == 6:
                return 'CONNECTOR'
            elif id == 7:
                return 'DIODE'
            elif id == 8:
                return 'DISPLAY'
            elif id == 9:
                return 'FUSE'
            elif id == 10:
                return 'INDUCTOR'
            elif id == 11:
                return 'POTENTIOMETER'
            elif id == 12:
                return 'RELAY'
            elif id == 13:
                return 'RESISTOR'
            elif id == 14:
                return 'SWITCH'
            elif id == 15:
                return 'TRANSISTOR'
            else:
                return None