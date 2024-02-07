import cv2
import numpy as np
from camera.camera import Camera
from segmentation.pcb_segmentor import PCBSegmentor
from common.common import rescale_image

#0. generacion de fotos:
#    1-5 luz natural ventana
#   6-10 luz artificila habitacion con persiana
#   11-15 luz focalizada
#   16-20 luz natura en otro momento

#1. Segementar las placas
#2. Segmentar las imagenes de las placas
#3. Detectar los componenetes
#4. Evaluar cuanto de bien esta la placa




def main():

    #VARIABLES

    #Parametros para la grabacion
    my_camera = Camera(hw_id=0, w=1280, h=720)
    #Modelos de deteccion
    pcb_segmentor = PCBSegmentor(trained = True)
    if pcb_segmentor.trained == False:
        pcb_segmentor.train()


    #PROCESADO

    #Flujo de streaming de imagenes se controla atraves de la variable recording
    frame, succes = my_camera.get_frame()
    recording = True
    while recording == True and succes == True:

        img_segmented_pcbs = []
        data_pcb = []

        #ADQUSICION

        #Recupera el frame de la camara
        frame, succes = my_camera.get_frame()
        h, w, _ = frame.shape

        #SEGMENTACION

        #Procesar el frame detectado por el segmentador de PCBs
        frame_pcb_detection, results_pcb = pcb_segmentor.run(frame)
    
        #Iteramos por los resultados
        for result in results_pcb:
            #Segemntado de la imagen
            if result.masks is not None:
                for mask in result.masks.data:
                    #Precesmos pl amsrcara para pdoer usarla
                    mask =  mask.detach().cpu().numpy() * 255
                    #La ajustamos a la imagen del frame
                    mask = cv2.resize(mask, (w, h))
                    #Aplicamos la mascara
                    frame_pcb_segmented = cv2.bitwise_and(frame, frame, mask=mask.astype(np.uint8))
                    #Añadrimos las pcbs detectadas
                    img_segmented_pcbs.append(frame_pcb_segmented)
            #df = result.pandas().xyxy[0]
            #for i in df['name']: # name->labels
                #dict = {'Label': , 'Position':, }
                #data_pcb.append(dict)
        
        #DETECCION

        #VISUALIZADO
        
        #Ensenar por pantana las distintas imagenes
        cv2.imshow('Result', frame_pcb_detection)
        if len(img_segmented_pcbs) > 0:
            cv2.imshow('Segmented_0', img_segmented_pcbs[0])
        
        #Espera a que se presione una tecla
        key = cv2.waitKey(1) & 0xFF
        #Si la tecla presionada es "q" se termina la grabacion
        if key == ord('q'):
            recording = False
            cv2.destroyWindow()

#TODO sistema de logs mas claro
#TODO usar logger Comet
#TODO stream = true, mirar com funciona y si eso implemntar, self.model.predict
    
if __name__ == "__main__":
    main()