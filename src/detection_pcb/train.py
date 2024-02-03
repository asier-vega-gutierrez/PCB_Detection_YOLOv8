from ultralytics import YOLO
import torch
import os

def train_pcb():

    #CONFIGURACION

    #Cargar el modelo
    model = YOLO("yolov8n.pt")
    #Modelo disponibles YOLOv8n < YOLOv8s < YOLOv8m < YOLOv8l < YOLOv8x
    
    #Enviar el modelo a al grafica
    print(f"Is CUDA supported by this system? {torch.cuda.is_available()}")
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(DEVICE)

    #ENTRNAMINETO

    #Entrenar el modelo
    model.train(data="./data/data_pcb/anotated/data.yaml", epochs=1)
  
    #GUARDADO

    #Guardado del modelo en onnx
    model.export(format='onnx')

    #Borramos el modelo original usado para que no estorbe
    os.remove("./yolov8n.pt")
    

    #TODO anadir evaluacion (model.eval ????)
    #TODO añadir crossvalidadcion
    #TODO usar logger Comet


if __name__ == '__main__': 
    train_pcb()
