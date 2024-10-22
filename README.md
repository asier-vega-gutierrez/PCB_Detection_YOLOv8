## Desarrollo de aplicación de visión por ordenador para entrenamiento y detección de PCBs y sus componentes con YOLOv8
<ul>
    <li>Fechas: Febrero 2024</li>
    <li>Descripción: Partiendo de múltiples PCBs se busca reentrenar la red neuronal YOLOv8 (https://github.com/ultralytics/ultralytics) con el objetivo de detectar PCBs y sus componentes. El proyecto se divide en dos modelos, el primero (yolov8n-seg.pt) clasifica el modelo de pcb entre los cuatro posibles (ARDUINO_MEGA = 0, ESP32 = 1, L298N =2, ULN2003 = 3) y segmenta la imagen para eliminar ruido. Después un segundo modelo (yolov8n.pt) detecta los componentes montados en cada PCB. Como resultado se evalua la precision general (n componentes detectados / n componente objetivo) y la precision de cada tipo componente detectado (ej: n condensadores detectados / n condensadores de dicha placa). 
</li>
    <li>Resultados:</li>
</ul>

![foto](https://github.com/asier-vega-gutierrez/PCB_Detection_YOLOv8/blob/main/doc/ImagenProceso.png)
