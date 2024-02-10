from ultralytics import YOLO
import torch
import os
from pathlib import Path
import json

'''Clase para detectar componentes'''
class ComponentDetector():

    def __init__(self, trained) -> None:
        self.model = None
        self.trained = trained

    '''Metodo de entrenamiento del modelo'''
    def train(self):

        #CONFIGURACION

        #Cargar el modelo
        self.model = YOLO("yolov8n.pt")
        #Modelo disponibles YOLOv8n < YOLOv8s < YOLOv8m < YOLOv8l < YOLOv8x
        
        #Enviar el modelo a al grafica
        print(f"Is CUDA supported by this system? {torch.cuda.is_available()}")
        DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(DEVICE)

        #Decidir si usar k-fold o no
        k_folds = False

        if k_folds == False:

            #ENTRNAMINETO

            #Entrenar el modelo
            self.model.train(data="./data/data_components/detected_0/data.yaml", epochs=50)
            
        else:

            #Cargar los datos
            ds_yamls = []
            save_path = Path('./data/data_components/detect_k_folds/Fold_Cross_val')
            for split in ['split_1', 'split_2', 'split_3']:
                split_dir = save_path / split
                dataset_yaml = split_dir / f'{split}_dataset.yaml'
                ds_yamls.append(dataset_yaml)

            #ENTRNAMIENTO

            #Entrenar el modelo
            batch = 16
            epochs = 10
            results = {}
            for k in range(3):
                dataset_yaml = ds_yamls[k]
                self.model.train(data=dataset_yaml, epochs=epochs, batch=batch)
                results[k] = self.model.metrics

        #Evaluacion del modelo
        self.model.val()
    
        #GUARDADO

        #Guardado del modelo en onnx
        self.model.export(format='onnx')

        #Borramos el modelo original usado para que no estorbe
        os.remove("./yolov8n.pt")
        
    '''Metodo para ejecutar el modelo'''
    def run(self, img):

        #CONFIGURACION

        #Cargar el modelo
        if self.model == None:
            print("Model is none loading the saved one")
            self.model = YOLO("./runs/good/train_component_detection_0/weights/best.pt")
            #Enviar el modelo a al grafica
            print(f"Is CUDA supported by this system? {torch.cuda.is_available()}")
            DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.model.to(DEVICE)

        #PROCESADO

        #Predecir una imagen (retina mask, para uqe devuelva mascaras para la segementacion)
        results = self.model.predict(img, save_conf=True)
        img = results[0].plot()
        
        #Devolver la imagen con la caja pintada
        return img, results
