from ultralytics import YOLO
import torch
import cv2

def main():

    #CONFIGURACION

    #Cargar el modelo
    model = YOLO("./runs/detect/train_detection_0/weights/best.pt")
    
    #Enviar el modelo a al grafica
    print(f"Is CUDA supported by this system? {torch.cuda.is_available()}")
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(DEVICE)

    #PRUEBAS

    #Predecir una imagen
    img = cv2.imread("./data/data_pcb/temp/arduino_mega/imagen_16.jpg")
    results = model(img)[0]
    img = results.plot()
    
    cv2.imshow('Result', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




if __name__ == '__main__': 
    main()