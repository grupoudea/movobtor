import cv2 as cv
import numpy as np

from seguidor import Seguidor

# 250, 415   390, 415
# 250,560   390,560

seguidor = Seguidor()

cap = cv.VideoCapture("video1-horizontal.mp4")
cap.get(cv.CAP_PROP_FPS)
deteccion = cv.createBackgroundSubtractorMOG2(history=10000, varThreshold=100)

# Definir los puntos para el cuadro
v_a = [250, 415]
v_b = [390, 415]
v_c = [390, 560]
v_d = [250, 560]

v_e = [970, 370]
v_f = [1117, 370]
v_g = [1117, 505]
v_h = [970, 505]

mascara = 0


def dibujar_area(a, b, c, d):
    pts = np.array([a, b, c, d], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=2)
    return pts

# dado un frame y aplicando filtros y operaciones morfologicas se obtiene el contorno
# "de un objeto en movimiento"
def configurar_contorno(frame):
    global mascara
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

# extraer del contorno cordenadas, alto y ancho y pinta un rectangulo al rededor del objeto detectado
def generar_detecciones(frame):
    detecciones = []
    contornos = configurar_contorno(frame)
    for contorno in contornos:
        area = cv.contourArea(contorno)
        if area > 5999:
            x, y, w, h = cv.boundingRect(contorno)
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)
            detecciones.append([x, y, w, h])
    return detecciones


def indicar_colision(pts, frame, cx, cy, x, y):
    area = cv.pointPolygonTest(pts, (cx, cy), False)
    if area >= 0:
        cv.circle(frame, (cx, cy), 3, (247, 17, 130), -1)
        cv.putText(frame, f'ENTRAMOS 1 (x, y): ({x}, {y})', (10, 30),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


def calcular_colision(coordenadas_contornos):
    for coordenada in coordenadas_contornos:
        x, y, ancho, alto, id = coordenada
        cv.putText(frame, f'({x},{y})', (x, y - 15), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)

        # pintamos rectangulo rojo
        # cv.rectangle(frame, (x, y - 10), (x + ancho, y + alto), (0, 0, 255), 2)
        cx = int(x + ancho / 2)
        cy = int(y + alto / 2)

        indicar_colision(pts, frame, cx, cy, x, y)
        indicar_colision(pts2, frame, cx, cy, x, y)


while True:
    ret, frame = cap.read() # lee un frame

    if not ret:
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        continue  # reiniciar la reproducción

    # pintar pixeles para el area
    pts = dibujar_area(v_a, v_b, v_c, v_d)
    pts2 = dibujar_area(v_e, v_f, v_g, v_h)

    detecciones = generar_detecciones(frame)

    coordenadas_contornos = seguidor.rastrear(detecciones)

    calcular_colision(coordenadas_contornos)

    # muestra el video
    cv.imshow("Video", frame)
    cv.imshow("Mascara", mascara)
    key = cv.waitKey(int(1000 / 25))  # Esperar 1 milisegundo
    if key == ord('q'):  # Presionar 'q' para salir del bucle
        break

# Liberar la cámara
cap.release()

# Cerrar todas las ventanas
cv.destroyAllWindows()
