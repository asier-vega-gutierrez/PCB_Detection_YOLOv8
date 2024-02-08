import cv2
import numpy as np
from camera.camera import Camera
from segmentation.pcb_segmentor import PCBSegmentor
from detection.component_detector import ComponentDetector
from common.common import is_inside_box

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
    #Modelo de segementacion
    pcb_segmentor = PCBSegmentor(trained = True)
    if pcb_segmentor.trained == False:
        pcb_segmentor.train()
    #Modelo de detecion
    component_detector = ComponentDetector(trained = True)
    if component_detector.trained == False:
        component_detector.train()

    #PROCESADO

    #Flujo de streaming de imagenes se controla atraves de la variable recording
    frame, succes = my_camera.get_frame()
    recording = True
    while recording == True and succes == True:

        img_segmented_pcb = None        #Imagen con todas las pcbs segmentadas
        results_pcb = None              #Resultados de la segmetnacion
        img_segmented_pcbs = []         #Imagenes de pcbs sin fondo
        data_segmented_pcb = []         #Informacion de las pcbs segmentadas
        
        img_detected_components = [] #Imagen con todos los componentes detectados 
        results_components = []      #Resultados de los compoentes detectados

        data_detected_components_pcbs = []   #Informacion de los componentes detectados por cada pcb

        data_full_pcbs = []         #Infromacion del resultado final de deteccion

        #ADQUSICION

        #Recupera el frame de la camara
        frame, succes = my_camera.get_frame()
        h, w, _ = frame.shape

        #SEGMENTACION

        #Procesar el frame detectado por el segmentador de PCBs
        img_segmented_pcb, results_pcb = pcb_segmentor.run(frame)
    
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
            #Extraccion de la informacion
            for box in result.boxes:
                #Extraermos la label y la caja
                dict = {'Label': int(box.cls[0].tolist()), 'Box':box.xyxy[0].tolist(), 'Components': []}
                #Añadimos los resultados a la lista
                data_segmented_pcb.append(dict)
        
        #DETECCION
        
        #Tenemos que itera por las imagens sin fondo para detectar los componentes
        if len(img_segmented_pcbs) > 0:
            for img in img_segmented_pcbs:
                #Ejecutamos la deteccion en cada imagen
                img, results = component_detector.run(img)
                #Guradmos las imagenes y los resultados
                img_detected_components.append(img)
                results_components.append(results)
        
        #Itereamos por los resultados
        for results in results_components:
            for result in results:
                #hay que iterar por las boxes de los componentes buscando si estas estan dentro de la box de la pcbs
                for id_pdb, pcb in enumerate(data_segmented_pcb):
                    for box in result.boxes:
                        #Si estan dentro de la pcb se añaden a la informacion anterior
                        if is_inside_box(pcb['Box'], box.xyxy[0].tolist()) == True:
                            pcb['Components'].append({'Label': int(box.cls[0].tolist()), 'Box': box.xyxy[0].tolist()})
                    #Se almacena la informacion completa de las pcbs
                    data_detected_components_pcbs.append(pcb)

        #Eliminamos los repetidos convierto el diccionario en tupla y comprandolos
        seen = set()
        for d in data_detected_components_pcbs:
            t = (d['Label'], tuple(d['Box']))
            if t not in seen:
                seen.add(t)
                data_full_pcbs.append(d)

        #VISUALIZADO
        
        #Ensenar por pantalla las distintas imagenes
        cv2.imshow('Result', img_segmented_pcb)
        if len(img_segmented_pcbs) > 0:
            cv2.imshow('Segmented_0', img_segmented_pcbs[0])
        if len(img_detected_components) > 0:
            cv2.imshow('Result_1', img_detected_components[0])
        
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