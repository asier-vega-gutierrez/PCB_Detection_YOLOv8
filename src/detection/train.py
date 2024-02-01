from ultralytics import YOLO
from torch.optim import Adam
from torch.optim.lr_scheduler import MultiStepLR
import torch





def main():

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
    model.train(data="./data/data_components/data.yaml", epochs=100)
  
    #TODO hacer que no genere el archvio yolov8n.pt
    #TODO anadir evaluacion
    #TODO añadir gruardado
    #TODO añadir crossvalidadcion


if __name__ == '__main__': 
    main()
