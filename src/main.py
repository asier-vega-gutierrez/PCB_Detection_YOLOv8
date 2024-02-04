import cv2
from camera.camera import Camera
from detection.pcb_detector import PCBDetector

#0. generacion de fotos:
#    1-5 luz natural ventana
#   6-10 luz artificila habitacion con persiana
#   11-15 luz focalizada

#1. Detectar las placas (clasificar el modelo ya)
#2. Segmentar las imagenes de las placas
#3. Detectar los componenetes
#4. Evaluar cuanto de bien esta la placa




def main():

    #VARIBLES

    #Parametor para la grabacion
    my_camera = Camera(hw_id=0, w=1280, h=720)
    #Modelos de deteccion
    pcb_detector = PCBDetector(trained = True)
    if pcb_detector.trained == False:
        pcb_detector.train()
    

    #PROCESADO

    #Flujo de striming de imagenes se controla atraves de la variable recording, por otro lado se peude para la ejecucion si la tecla "P" se mantiene pulsada
    frame, succes = my_camera.get_frame()
    recording = True
    while recording == True and succes == True:

        #ADQUSICION

        #Recupera el frame de la camara
        frame, succes = my_camera.get_frame()

        #DETECCION

        frame = pcb_detector.run(frame)
        cv2.imshow('Result', frame)
        

        #Espera a que se presione una tecla
        key = cv2.waitKey(1) & 0xFF
        #Si la tecla presionada es "q" se termina la grabacion
        if key == ord('q'):
            recording = False

    
#TODO sistema de logs mas claro
    
if __name__ == "__main__":
    main()