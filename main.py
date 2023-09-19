import time

import numpy as np
import cv2 as cv

from seguidor import Seguidor

carI = {}
carO = {}
pruebas = {}

# 250, 415   390, 415
# 250,560   390,560

seguidor = Seguidor()

cap = cv.VideoCapture("video1-horizontal-slow.mp4")
deteccion = cv.createBackgroundSubtractorMOG2(history=10000, varThreshold=100)

while True:

    ret, frame = cap.read()

    if frame is not None:
        height, width = frame.shape[:2]
        print("height", height)
        print("width", width)

    if not ret:
        # El video ha terminado, reiniciar la reproducción
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        continue  # Continuar desde el principio



    mask = np.zeros((height, width), dtype=np.uint8)

    # Definir los puntos para el cuadro
    pts = np.array([[250, 415], [390, 415], [390, 560], [250, 560]], np.int32)
    pts = pts.reshape((-1, 1, 2))

    pts2 = np.array([[970, 370], [1117, 370], [1117, 505], [970, 505]], np.int32)
    pts2 = pts2.reshape((-1, 1, 2))

    # Dibujar el cuadro
    cv.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=2)
    cv.polylines(frame, [pts2], isClosed=True, color=(255, 0, 0), thickness=2)

    mascara = deteccion.apply(frame)
    filtro = cv.GaussianBlur(mascara, (11, 11), 0)

    # umbral
    _, umbral = cv.threshold(filtro, 50, 255, cv.THRESH_BINARY)

    # dilatamos
    dilatacion = cv.dilate(umbral, np.ones((3, 3)))

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))

    cierre = cv.morphologyEx(dilatacion, cv.MORPH_CLOSE, kernel)

    contornos, _ = cv.findContours(cierre, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    detecciones = []

    for contorno in contornos:
        area = cv.contourArea(contorno)
        print("AREAW: ", area)
        if area > 5999:
            x, y, w, h = cv.boundingRect(contorno)
            print("detectando rec: x,y,w,h", x, y, w, h)
            cv.rectangle(frame, (x,y), (x+w, y+h), (255,255,0), 3)
            detecciones.append([x, y, w, h])

    objecto_id = seguidor.rastrear(detecciones)

    for objeto in objecto_id:
        x, y, ancho, alto, id = objeto
        cv.putText(frame, f'({x},{y})', (x,y-15), cv.FONT_HERSHEY_PLAIN, 1, (0,255,255), 2)

        print("pintando rec: x,y,w,h", x, y, ancho, alto)
        # pintamos rectangulo rojo
        # cv.rectangle(frame, (x, y - 10), (x + ancho, y + alto), (0, 0, 255), 2)
        cx = int(x + ancho / 2)
        cy = int(y + alto / 2)
        print("Centro en x=", cx, "centro en y=", cy)

        a2 = cv.pointPolygonTest(pts, (cx, cy), False)
        a3 = cv.pointPolygonTest(pts2, (cx, cy), False)
        print("a2: ", a2)

        if a2 >= 0:
            cv.circle(frame, (cx, cy), 3, (247, 17, 130), -1)
            cv.putText(frame, f'ENTRAMOS 1 (x, y): ({x}, {y})', (10, 30),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if a3 >= 0:
            cv.circle(frame, (cx, cy), 3, (247, 17, 130), -1)
            cv.putText(frame, f'ENTRAMOS 2 (x, y): ({x}, {y})', (10, 30),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # muestra el video
    cv.imshow("Video", frame)
    cv.imshow("Frame alterado", cierre)

    key = cv.waitKey(int(1000/25))  # Esperar 1 milisegundo

    if key == ord('q'):  # Presionar 'q' para salir del bucle
        break

    # Espera durante un número de segundos definido en 'tiempo_espera'
    time.sleep(2)

# Liberar la cámara
cap.release()

# Cerrar todas las ventanas
cv.destroyAllWindows()
