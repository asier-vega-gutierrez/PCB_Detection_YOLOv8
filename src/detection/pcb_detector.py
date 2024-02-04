from ultralytics import YOLO
import torch
import cv2
import os

class PCBDetector():

    def __init__(self, trained) -> None:
        self.model = None
        self.trained = trained

    def train(self):

        #CONFIGURACION

        #Cargar el modelo
        self.model = YOLO("yolov8n.pt")
        #Modelo disponibles YOLOv8n < YOLOv8s < YOLOv8m < YOLOv8l < YOLOv8x
        
        #Enviar el modelo a al grafica
        print(f"Is CUDA supported by this system? {torch.cuda.is_available()}")
        DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(DEVICE)

        #ENTRNAMINETO

        #Entrenar el modelo
        self.model.train(data="./data/data_pcb/anotated/data.yaml", epochs=50)

        #Evaluacion del modelo
        self.model.val()
    
        #GUARDADO

        #Guardado del modelo en onnx
        self.model.export(format='onnx')

        #Borramos el modelo original usado para que no estorbe
        os.remove("./yolov8n.pt")
        

        #TODO añadir crossvalidadcion https://docs.ultralytics.com/guides/kfold-cross-validation/
        #TODO usar logger Comet
    
    def run(self, img):

        #CONFIGURACION

        #Cargar el modelo
        if self.model == None:
            self.model = YOLO("./runs/good/train_pcb_0/weights/best.pt")
             #Enviar el modelo a al grafica
            print(f"Is CUDA supported by this system? {torch.cuda.is_available()}")
            DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.model.to(DEVICE)

        #PROCESADO

        #Predecir una imagen
        results = self.model(img)[0]
        img = results.plot()
        
        return img