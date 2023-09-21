import time
import numpy as np
import cv2 as cv

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
tiempo_entra_area = 0

v_a = [90, 0]
v_b = [1094, 0]
v_c = [1094, 720]
v_d = [90, 720]


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


tiempo_inicial = 0
tiempo_final = 0
primer_frame = True
frame_anterior = True

# [id, ti, tf, xi, xf, v, a]
vector_velocidad = {}
idFrameAnterior = 0

while True:
    ret, frame = cap.read()

    if not ret:
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        vector_velocidad = {}
        primer_frame = True
        frame_anterior = True
        continue  # reiniciar la reproducción

    pts = dibujar_area(v_a, v_b, v_c, v_d)

    contornos = configurar_contorno(frame)
    detecciones = []

    for contorno in contornos:
        area = cv.contourArea(contorno)
        if area > 1000:
            x, y, w, h = cv.boundingRect(contorno)
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)
            detecciones.append([x, y, w, h])

    coordenadas_contornos = seguidor.rastrear(detecciones)

    if frame is not None:
        height, width = frame.shape[:2]

    for coordenada in coordenadas_contornos:
        x, y, ancho, alto, id = coordenada

        if height == alto or width == ancho:
            continue

        # cv.putText(frame, f'({x},{y})', (x, y - 15), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
        print("x=",x)
        cx = int(x + ancho / 2)
        cy = int(y + alto / 2)

        a2 = cv.pointPolygonTest(pts, (cx, cy), False)

        if x + ancho >= 90 and frame_anterior:
            frame_anterior = False
            tiempo_entra_area = time.time()

        if a2 >= 0:
            cv.circle(frame, (cx, cy), 3, (247, 17, 130), -1)

            if primer_frame:
                primer_frame = False
                tiempo_inicial = 0
                distancia_inicial_cm = 0

            else:
                _, tiempo_final_anterior, _, distancia_final_anterior, _ = vector_velocidad[idFrameAnterior]
                tiempo_inicial = tiempo_final_anterior
                distancia_inicial_cm = distancia_final_anterior

            tiempo_final = time.time() - tiempo_entra_area

            distancia_px = x - punto_inicial
            distancia_final_cm = (distancia_px*total_area_cm)/ancho_area_interes

            velocidad_instantanea = 0
            if (tiempo_final - tiempo_inicial) > 0:
                velocidad_instantanea = (distancia_final_cm - distancia_inicial_cm) / (tiempo_final - tiempo_inicial)

            vector_velocidad[id] = (
            tiempo_inicial, tiempo_final, distancia_inicial_cm, distancia_final_cm, velocidad_instantanea)
            idFrameAnterior = id

            cv.putText(frame, f'{velocidad_instantanea} cm/s', (x, y - 15), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)

        else:
            print("No esta en el area")

    print("tiempo_inicial = ", tiempo_inicial)
    print("tiempo_final = ", tiempo_final)
    print("vector_velocidad = ", vector_velocidad)

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
