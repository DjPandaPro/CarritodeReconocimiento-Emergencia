import cv2  # OpenCV
import urllib.request  # Para abrir y leer URL
import numpy as np
import os

# URL de la cámara IP (ajustar según tu configuración)
#url = 'http://192.168.18.119/cam-hi.jpg'
url = 'http://192.168.0.142/cam-hi.jpg'
winName = 'ESP32 CAMERA'
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)

# Ruta base (ajustar según tu ubicación de archivos)
base_path = r'C:\Users\Usuario\Desktop\Proyectos Arduino\yfy\esp32cam-IA-main'
classFile = os.path.join(base_path, 'coco.names')
configPath = os.path.join(base_path, 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
weightsPath = os.path.join(base_path, 'frozen_inference_graph.pb')

# Cargar nombres de clases
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# Configurar modelo de detección
net = cv2.dnn.DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# Archivo para registrar todas las detecciones
registro_detecciones = os.path.join(base_path, "detecciones.txt")

while True:
    try:
        # Leer imagen desde la cámara IP
        imgResponse = urllib.request.urlopen(url)
        imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)

        # Detectar objetos en la imagen
        detections = net.detect(img, confThreshold=0.5)
        classIds, confs, bbox = detections if len(detections) == 3 else (None, None, None)

        # Procesar detecciones
        if classIds is not None and len(classIds) > 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                label = classNames[classId - 1]
                confidence_text = f"{label}: {confidence:.2f}"
                cv2.rectangle(img, box, color=(0, 255, 0), thickness=3)
                cv2.putText(img, confidence_text, (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                # Registrar la detección en el archivo
                with open(registro_detecciones, 'a') as registro:
                    registro.write(f"{confidence_text}\n")

        # Mostrar imagen procesada
        cv2.imshow(winName, img)

        # Terminar el programa al presionar ESC
        tecla = cv2.waitKey(5) & 0xFF
        if tecla == 27:
            break
    except Exception as e:
        print(f"Error: {e}")
        break

cv2.destroyAllWindows()
