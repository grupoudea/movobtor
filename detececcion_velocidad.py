import time

import cv2 as cv
import numpy as np

from grafica import generar_grafica_distancia_x_tiempo, generar_grafica_velocidad_x_tiempo
from seguidor import Seguidor

deteccion = cv.createBackgroundSubtractorMOG2(history=10000, varThreshold=100)

seguidor = Seguidor()

# 90,0   90, 720
# 1094,0   1094,720

punto_inicial = 0

is_primer_frame = True
is_frame_anterior = True
is_velocidad_inicial = True
tiempo_entra_area = 0
idFrameAnterior = 0
velocidad_punto_inicial = 0

# [id, ti, tf, xi, xf, vi, vf, a]
# vector_velocidad = {}


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


def dibujar_area(a, b, c, d, frame):
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
    return tiempo_entra_area


def get_tiempo_distancia_inicial(vector_velocidad):
    global is_primer_frame
    if is_primer_frame:
        is_primer_frame = False
        tiempo_inicial = 0
        distancia_inicial_cm = 0
    else:
        _, tiempo_final_anterior, _, distancia_final_anterior, _, _, _ = vector_velocidad[idFrameAnterior]
        tiempo_inicial = tiempo_final_anterior
        distancia_inicial_cm = distancia_final_anterior

    return tiempo_inicial, distancia_inicial_cm


def get_tiempo_distancia_final(x, ancho_frame_cm, distancia_cm):
    tiempo_final = time.time() - tiempo_entra_area
    distancia_px = x - punto_inicial
    distancia_final_cm = parse_px_to_cm(distancia_px, ancho_frame_cm, distancia_cm)
    return tiempo_final, distancia_final_cm


def get_velocidad_inicial(velocidad_punto_inicial, vector_velocidad):
    global is_velocidad_inicial
    if is_velocidad_inicial:
        is_velocidad_inicial = False
        velocidad_inicial = velocidad_punto_inicial
    else:
        _, _, _, _, _, velocidad_final_anterior, _ = vector_velocidad[idFrameAnterior]
        velocidad_inicial = velocidad_final_anterior
    return velocidad_inicial


def parse_px_to_cm(distancia_px, ancho_frame_px, distancia_cm):
    return (distancia_px * distancia_cm) / ancho_frame_px


def get_velocidad_instantanea(ti, tf, di, df):
    velocidad_instantanea = 0
    if (tf - ti) > 0:
        velocidad_instantanea = (df - di) / (tf - ti)
    return velocidad_instantanea


def get_aceleracion(ti, tf, vi, vf):
    aceleracion = 0
    if (tf - ti) > 0:
        aceleracion = (vf - vi) / (tf - ti)
    return aceleracion


def calcular_velocidad_inicial(x, ancho_frame_px, distancia_cm):
    tiempo_inicial_i = 0
    tiempo_final_i = time.time()
    distancia_inicial_i = 0
    distancia_final_i_px = x
    distancia_final_cm = parse_px_to_cm(distancia_final_i_px, ancho_frame_px, distancia_cm)
    velocidad = get_velocidad_instantanea(tiempo_inicial_i, tiempo_final_i, distancia_inicial_i, distancia_final_cm)
    return velocidad


def calcular_vector_velocidad(frame, coordenadas_contornos, pts, vector_velocidad, distancia_cm):
    global tiempo_entra_area, idFrameAnterior, is_velocidad_inicial, velocidad_punto_inicial

    if frame is not None:
        height, width = frame.shape[:2]
        print(f"h={height} w={width}")

    for coordenada in coordenadas_contornos:
        x, y, ancho, alto, id = coordenada

        # validar si el objeto capturado es el frame total
        if height == alto or width == ancho:
            continue

        if x <= punto_inicial and (frame is not None):
            is_velocidad_inicial = True
            velocidad_punto_inicial = calcular_velocidad_inicial(x, width, distancia_cm)

        # calcular los centros
        cx = int(x + ancho / 2)
        cy = int(y + alto / 2)

        # obtener el momento en que el objeto entra al area
        tiempo_entra_area = get_tiempo_entra_area(x, ancho)

        a2 = cv.pointPolygonTest(pts, (cx, cy), False)
        if a2 >= 0:
            cv.circle(frame, (cx, cy), 3, (247, 17, 130), -1)

            tiempo_inicial, distancia_inicial = get_tiempo_distancia_inicial(vector_velocidad)
            tiempo_final, distancia_final = get_tiempo_distancia_final(x, width, distancia_cm)
            velocidad_inicial = get_velocidad_inicial(velocidad_punto_inicial, vector_velocidad)

            velocidad_final = get_velocidad_instantanea(tiempo_inicial, tiempo_final,
                                                        distancia_inicial, distancia_final)

            aceleracion = get_aceleracion(tiempo_inicial, tiempo_final, velocidad_inicial, velocidad_final)

            vector_velocidad[id] = (
                tiempo_inicial, tiempo_final,
                distancia_inicial, distancia_final,
                velocidad_inicial, velocidad_final,
                aceleracion
            )
            idFrameAnterior = id

            cv.putText(frame, f'{round(velocidad_final, 2)} cm/s', (x, y - 15), cv.FONT_HERSHEY_SIMPLEX, 1,
                       (0, 255, 255), 2)
            cv.putText(frame, f'{round(aceleracion, 4)} cm/s^2', (x, y - 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255),
                       2)

            return vector_velocidad


def procesar_video(path, distancia_cm):
    cap = cv.VideoCapture(path)
    fps = cap.get(cv.CAP_PROP_FPS)
    vector_velocidad = {}

    print("fps: ", fps)

    while True:
        ret, frame = cap.read()

        if not ret:
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            generar_grafica_distancia_x_tiempo(vector_velocidad)
            generar_grafica_velocidad_x_tiempo(vector_velocidad)
            is_primer_frame = True
            is_frame_anterior = True
            vector_velocidad = {}
            tiempo_entra_area = 0
            break  # reiniciar la reproducción

        height, width = frame.shape[:2]
        v_a = [0, 0]
        v_b = [width, 0]
        v_c = [width, height]
        v_d = [0, height]

        pts = dibujar_area(v_a, v_b, v_c, v_d, frame)

        detecciones = generar_detecciones(frame)

        coordenadas_contornos = seguidor.rastrear(detecciones)

        calcular_vector_velocidad(frame, coordenadas_contornos, pts, vector_velocidad, distancia_cm)

        if vector_velocidad:
            print("vector_velocidad = ", vector_velocidad)

        # Muestra el video
        if frame is not None:
            cv.imshow("Video", frame)
        else:
            break

        key = cv.waitKey(120)  # Esperar 1 milisegundo

        if key == ord('q'):  # Presionar 'q' para salir del bucle
            break

        # time.sleep(1.5)

    # Liberar la cámara
    cap.release()
    # Cerrar todas las ventanas
    cv.destroyAllWindows()

procesar_video("video1280-horizontal.mp4", 90)
