import cv2
from camera.camera import Camera

# Función para guardar la imagen actual con un nombre único
def guardar_imagen(frame, contador):
    nombre_archivo = f'imagen_{contador}.jpg'
    cv2.imwrite(nombre_archivo, frame)
    print(f'Imagen guardada como {nombre_archivo}')
    return contador + 1

# Inicializa el contador
contador = 1
# Configuracion de la camara
my_camera = Camera(hw_id=0, w=1280, h=720)

while True:
    # Captura el fotograma actual
    frame, succes = my_camera.get_frame()

    # Muestra el fotograma en una ventana llamada "Frame"
    cv2.imshow('Frame', frame)

    # Tamaño de la imagen gravada
    #print(frame.shape)

    # Espera a que se presione una tecla
    key = cv2.waitKey(1) & 0xFF

    # Si la tecla presionada es "s", guarda la imagen actual y actualiza el contador
    if key == ord('s'):
        contador = guardar_imagen(frame, contador)
    # Si la tecla presionada es "q", sale del bucle
    elif key == ord('q'):
        break

# Libera la captura y cierra la ventana
cv2.destroyAllWindows()