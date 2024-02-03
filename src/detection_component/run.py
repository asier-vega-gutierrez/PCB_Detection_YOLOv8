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
    
    cv2.imshow('Result', rescale_image(img, 100))
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def rescale_image(img, scale_percent):

    # Get the original width and height
    original_width, original_height = img.shape[1], img.shape[0]

    # Calculate the new width and height based on the scale percentage
    new_width = int(original_width * scale_percent / 100)
    new_height = int(original_height * scale_percent / 100)

    # Resize the image
    resized_image = cv2.resize(img, (new_width, new_height))

    return resized_image

if __name__ == '__main__': 
    main()