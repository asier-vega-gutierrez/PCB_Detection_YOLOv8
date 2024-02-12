
"""Clase con todas las constantes"""
class Constants:
    
    def __init__(self) -> None:

        #Constantes de pcbs
        self.ARDUINO_MEGA = 0
        self.ESP32 = 1
        self.L298N = 2
        self.ULN2003 = 3 # 

        #Nuemro de componente de cada pcb RECONTAR #################
        self.ARDUINO_MEGA_COUNT = 56
        self.ESP32_COUNT = 31
        self.L298N_COUNT = 21
        self.ULN2003_COUNT = 13 
        
        #Constantes de componentes
        self.IC = 0 #
        self.LED = 1 #
        self.BATTERY = 2 #
        self.BUZZER = 3 #
        self.CAPACITOR = 4 #
        self.CLOCK = 5 #
        self.CONNECTOR = 6 #
        self.DIODE = 7 #
        self.DISPLAY = 8 #
        self.FUSE = 9 #
        self.INDUCTOR = 10 #
        self.POTENTIOMETER = 11 #
        self.RELAY = 12 #
        self.RESISTOR = 13
        self.SWITCH = 14 #
        self.TRANSISTOR = 15 #

        #Constantes de componentes por pcb
        self.ARDUINO_MEGA_COMPONENTS = {self.SWITCH: 1, self.CAPACITOR: 19, self.CLOCK: 2, self.CONNECTOR: 11, self.DIODE: 2, self.FUSE: 1, self.IC: 7, self.LED: 4, self.RESISTOR: 9}
        self.ESP32_COMPONENTS = {self.RESISTOR: 10, self.IC: 6, self.LED: 1, self.CAPACITOR: 7, self.CONNECTOR: 3, self.DIODE: 1, self.TRANSISTOR: 1, self.SWITCH: 2}
        self.L298N_COMPONENTS = {self.IC: 2, self.LED: 1, self.CAPACITOR: 2, self.RESISTOR: 1, self.DIODE: 8, self.CONNECTOR: 7}
        self.ULN2003_COMPONENTS = {self.IC: 1, self.CONNECTOR: 3, self.RESISTOR: 4, self.LED: 4, self.CAPACITOR: 1}