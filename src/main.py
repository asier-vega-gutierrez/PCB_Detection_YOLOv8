import cv2
import numpy as np
from camera.camera import Camera
from segmentation.pcb_segmentor import PCBSegmentor
from detection.component_detector import ComponentDetector
from screen.display_3x3 import display3x3
from common.common import is_inside_box
from common.common import count_occurrences
from common.common import component_accuracy
from static.constants import Constants


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
    #Constantes
    const = Constants()

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
                dict = {'Label': int(box.cls[0].tolist()), 'Box':box.xyxy[0].tolist(), 'Components': [], 'Accuracy': 0.0, 'Accuracy_by_component': []}
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

        #RESULTADOS
                
        #Iterar por cada pcb detectada
        if len(data_full_pcbs) > 0:
            for id_pcb, pcb in enumerate(data_full_pcbs):
                #Sabiendo en que pcb trabajamos
                if pcb['Label'] == 0:
                    general_acuracy_100 = const.ARDUINO_MEGA_COUNT
                    actual_labels = const.ARDUINO_MEGA_COMPONENTS
                elif pcb['Label'] == 1:
                    general_acuracy_100 = const.ESP32_COUNT
                    actual_labels = const.ESP32_COMPONENTS
                elif pcb['Label'] == 2:
                    general_acuracy_100 = const.L298N_COUNT
                    actual_labels = const.L298N_COMPONENTS
                elif pcb['Label'] == 3:
                    general_acuracy_100 = const.ULN2003_COUNT
                    actual_labels = const.ULN2003_COMPONENTS
                #Alamcenar los compoenentes detectados de la pcb
                actual_components = []
                for component in pcb['Components']:
                    actual_components.append(component['Label'])
                #Precicsion general: numero de conponentes totaltes
                count_components = len(actual_components)
                pcb['Accuracy'] = count_components / general_acuracy_100
                #Precision de componente: numero de componentes de cada tipo
                occurrence_components = count_occurrences(actual_components)
                print(component_accuracy(occurrence_components, actual_labels))
                pcb['Accuracy_by_component'] = component_accuracy(actual_labels, occurrence_components)
                #Añadimos los datos a la lsita principal
                data_full_pcbs[id_pcb] = pcb         

        #VISUALIZADO
        
        #Pintamos la informacion por pantalla
        display3x3('Actual Frame', frame, 1)
        display3x3('Segemented pcbs', img_segmented_pcb, 4)
        if len(img_segmented_pcbs) > 0:
            display3x3('Pcb no backgorund' , img_segmented_pcbs[0], 5)
        if len(img_detected_components) > 0:
            cv2.putText(img_detected_components[0], "Genal precision: "+ str(round(data_full_pcbs[0]['Accuracy'], 2)), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(img_detected_components[0], "Component precision: "+ str(data_full_pcbs[0]['Accuracy_by_component']), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            display3x3('Pcb components' , img_detected_components[0], 7)
        
        #Espera a que se presione una tecla
        key = cv2.waitKey(1) & 0xFF
        #Si la tecla presionada es "q" se termina la grabacion
        if key == ord('q'):
            recording = False
            cv2.destroyWindow(0)
    
if __name__ == "__main__":
    main()