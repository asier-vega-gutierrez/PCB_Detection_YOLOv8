from ultralytics import YOLO
import torch


def train_pcb():

    #CONFIGURACION

    #Cargar el modelo
    model = YOLO("./model/original/yolov8n.pt")
    #Modelo disponibles YOLOv8n < YOLOv8s < YOLOv8m < YOLOv8l < YOLOv8x
    
    #Enviar el modelo a al grafica
    print(f"Is CUDA supported by this system? {torch.cuda.is_available()}")
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(DEVICE)

    #ENTRNAMINETO

    #Entrenar el modelo
    model.train(data="./data/data_pcb/anotated/data.yaml", epochs=1)
  
    #TODO hacer que no genere el archvio yolov8n.pt
    #TODO anadir evaluacion
    #TODO añadir gruardado
    #TODO añadir crossvalidadcion


if __name__ == '__main__': 
    train_pcb()
