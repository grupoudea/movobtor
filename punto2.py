import time

import cv2 as cv
import numpy as np

from grafica import generar_grafica
from seguidor import Seguidor

seguidor = Seguidor()

cap = cv.VideoCapture("video1280-horizontal.mp4")
fps = cap.get(cv.CAP_PROP_FPS)
print("fps: ", fps)
deteccion = cv.createBackgroundSubtractorMOG2(history=10000, varThreshold=100)

# 90,0   90, 720
# 1094,0   1094,720

punto_inicial = 90
punto_final = 1094
ancho_video_total = 1280
ancho_area_interes = punto_final - punto_inicial
ancho_en_cm = 90
total_area_cm = (ancho_en_cm * ancho_area_interes) / ancho_video_total

v_a = [90, 0]
v_b = [1094, 0]
v_c = [1094, 720]
v_d = [90, 720]

is_primer_frame = True
is_frame_anterior = True
tiempo_entra_area = 0
idFrameAnterior = 0

# [id, ti, tf, xi, xf, v, a]
vector_velocidad = {}


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


def dibujar_area(a, b, c, d):
    pts = np.array([a, b, c, d], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=2)
    return pts


def generar_detecciones(frame):
    detecciones = []
    contornos = configurar_contorno(frame)
    for contorno in contornos:
        area = cv.contourArea(contorno)
        if area > 1000:
            x, y, w, h = cv.boundingRect(contorno)
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)
            detecciones.append([x, y, w, h])
    return detecciones


def get_tiempo_entra_area(x, ancho):
    global is_frame_anterior, tiempo_entra_area
    if x + ancho >= punto_inicial and is_frame_anterior:
        is_frame_anterior = False
        tiempo_entra_area = time.time()
    print("tiempo_entra_area=",tiempo_entra_area)
    return tiempo_entra_area


def get_tiempo_distancia_inicial():
    global is_primer_frame
    if is_primer_frame:
        is_primer_frame = False
        tiempo_inicial = 0
        distancia_inicial_cm = 0
    else:
        _, tiempo_final_anterior, _, distancia_final_anterior, _ = vector_velocidad[idFrameAnterior]
        tiempo_inicial = tiempo_final_anterior
        distancia_inicial_cm = distancia_final_anterior

    return tiempo_inicial, distancia_inicial_cm


def get_tiempo_distancia_final(x):
    tiempo_final = time.time() - tiempo_entra_area
    distancia_px = x - punto_inicial
    distancia_final_cm = (distancia_px * total_area_cm) / ancho_area_interes
    return tiempo_final, distancia_final_cm


def get_velocidad_instantanea(tiempo_inicial, tiempo_final, distancia_inicial_cm, distancia_final_cm):
    velocidad_instantanea = 0
    if (tiempo_final - tiempo_inicial) > 0:
        velocidad_instantanea = (distancia_final_cm - distancia_inicial_cm) / (tiempo_final - tiempo_inicial)
    return velocidad_instantanea


def calcular_vector_velocidad(frame, coordenadas_contornos, pts):
    global tiempo_entra_area, idFrameAnterior

    if frame is not None:
        height, width = frame.shape[:2]

    for coordenada in coordenadas_contornos:
        x, y, ancho, alto, id = coordenada

        # validar si el objeto capturado es el frame total
        if height == alto or width == ancho:
            continue

        # calcular los centros
        cx = int(x + ancho / 2)
        cy = int(y + alto / 2)

        # obtener el momento en que el objeto entra al area
        tiempo_entra_area = get_tiempo_entra_area(x, ancho)

        a2 = cv.pointPolygonTest(pts, (cx, cy), False)
        if a2 >= 0:
            cv.circle(frame, (cx, cy), 3, (247, 17, 130), -1)

            tiempo_inicial, distancia_inicial = get_tiempo_distancia_inicial()
            tiempo_final, distancia_final = get_tiempo_distancia_final(x)

            velocidad_instantanea = get_velocidad_instantanea(tiempo_inicial, tiempo_final,
                                                              distancia_inicial, distancia_final)

            vector_velocidad[id] = (
                tiempo_inicial, tiempo_final,
                distancia_inicial, distancia_final,
                velocidad_instantanea
            )
            idFrameAnterior = id

            cv.putText(frame, f'{velocidad_instantanea} cm/s', (x, y - 15), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)


while True:
    ret, frame = cap.read()

    if not ret:
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        generar_grafica(vector_velocidad)
        is_primer_frame = True
        is_frame_anterior = True
        vector_velocidad = {}
        tiempo_entra_area = 0
        continue  # reiniciar la reproducción

    pts = dibujar_area(v_a, v_b, v_c, v_d)

    detecciones = generar_detecciones(frame)

    coordenadas_contornos = seguidor.rastrear(detecciones)

    calcular_vector_velocidad(frame, coordenadas_contornos, pts)

    # print("vector_velocidad = ", vector_velocidad)

    # Muestra el video
    if frame is not None:
        cv.imshow("Video", frame)
    else:
        break

    key = cv.waitKey(int(1000 / fps))  # Esperar 1 milisegundo

    if key == ord('q'):  # Presionar 'q' para salir del bucle
        break

    # time.sleep(1)

# Liberar la cámara
cap.release()

# Cerrar todas las ventanas
cv.destroyAllWindows()
