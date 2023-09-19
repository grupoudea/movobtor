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

v_a = [250, 415]
v_b = [390, 415]
v_c = [390, 560]
v_d = [250, 560]

v_e = [970, 370]
v_f = [1117, 370]
v_g = [1117, 505]
v_h = [970, 505]

def get_dimensions(frame):
    if frame is not None:
        height, width = frame.shape[:2]
        return height, width
    else:
        return None

def dibujar_cuadro(a, b, c, d):
    pts = np.array([a, b, c, d], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=2)
    return pts

def configurar_contorno(frame):
    mascara = deteccion.apply(frame)
    filtro = cv.GaussianBlur(mascara, (11, 11), 0)

    # umbral
    _, umbral = cv.threshold(filtro, 50, 255, cv.THRESH_BINARY)

    # dilatamos
    dilatacion = cv.dilate(umbral, np.ones((3, 3)))
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    cierre = cv.morphologyEx(dilatacion, cv.MORPH_CLOSE, kernel)
    contornos, _ = cv.findContours(cierre, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return contornos

def indicar_colision(pts, frame, cx, cy, x, y):
    area = cv.pointPolygonTest(pts, (cx, cy), False)
    if area >= 0:
        cv.circle(frame, (cx, cy), 3, (247, 17, 130), -1)
        cv.putText(frame, f'ENTRAMOS 1 (x, y): ({x}, {y})', (10, 30),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

while True:

    ret, frame = cap.read()

    if not ret:
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        continue  # reiniciar la reproducción

    height, width = get_dimensions(frame)

    mask = np.zeros((height, width), dtype=np.uint8)

    # Definir los puntos para el cuadro
    pts = dibujar_cuadro(v_a, v_b, v_c, v_d)
    pts2 = dibujar_cuadro(v_e, v_f, v_g, v_h)

    detecciones = []

    contornos = configurar_contorno(frame)
    for contorno in contornos:
        area = cv.contourArea(contorno)
        if area > 50:
            x, y, w, h = cv.boundingRect(contorno)
            print("detectando rec: x,y,w,h", x, y, w, h)
            detecciones.append([x, y, w, h])

    objecto_id = seguidor.rastrear(detecciones)

    for objeto in objecto_id:
        x, y, ancho, alto, id = objeto

        print("pintando rec: x,y,w,h", x, y, ancho, alto)
        cv.rectangle(frame, (x, y - 10), (x + ancho, y + alto), (0, 0, 255), 2)
        cx = int(x + ancho / 2)
        cy = int(y + alto / 2)
        print("Centro en x=", cx, "centro en y=", cy)

        indicar_colision(pts, frame, cx, cy, x, y)
        indicar_colision(pts2, frame, cx, cy, x, y)


    # muestra el video
    cv.imshow("Video", frame)
    # cv.imshow("Frame alterado", cierre)

    key = cv.waitKey(1)  # Esperar 1 milisegundo

    if key == ord('q'):  # Presionar 'q' para salir del bucle
        break

    # Espera durante un número de segundos definido en 'tiempo_espera'
    time.sleep(0.25)

# Liberar la cámara
cap.release()

# Cerrar todas las ventanas
cv.destroyAllWindows()
