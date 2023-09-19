import time
import numpy as np
import cv2 as cv
from seguidor import Seguidor

seguidor = Seguidor()

cap = cv.VideoCapture("videoPunto2-horizontal1.mp4")
fps = cap.get(cv.CAP_PROP_FPS)
print("fps: ", fps)
deteccion = cv.createBackgroundSubtractorMOG2(history=10000, varThreshold=100)

# 90,0   90, 720
# 1094,0   1094,720

# Medida conocida en el video (en píxeles) y su correspondiente en el mundo real (en cm)
distancia_pixeles = 100
distancia_cm = 10

# Calcula la relación píxeles/cm
relacion_pixeles_cm = distancia_pixeles / distancia_cm

while True:
    ret, frame = cap.read()

    if not ret:
        # El video ha terminado, reiniciar la reproducción
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        continue  # Continuar desde el principio

    if frame is not None:
        height, width = frame.shape[:2]
        print("height", height)
        print("width", width)
    else:
        break  # Ignorar frames vacíos o con dimensiones no válidas

    mask = np.zeros((height, width), dtype=np.uint8)

    # Definir los puntos para el cuadro
    pts = np.array([[90, 0], [90, 720], [1094, 720], [1094, 0]], np.int32)
    pts = pts.reshape((-1, 1, 2))

    # Dibujar el cuadro
    cv.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=2)

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
        if area > 2000:
            x, y, w, h = cv.boundingRect(contorno)
            print("detectando rec: x,y,w,h", x, y, w, h)
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)
            detecciones.append([x, y, w, h])

    objecto_id = seguidor.rastrear(detecciones)

    for objeto in objecto_id:
        x, y, ancho, alto, id = objeto
        cv.putText(frame, f'({x},{y})', (x, y - 15), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)

        print("pintando rec: x,y,w,h", x, y, ancho, alto)
        # pintamos rectangulo rojo
        # cv.rectangle(frame, (x, y - 10), (x + ancho, y + alto), (0, 0, 255), 2)
        cx = int(x + ancho / 2)
        cy = int(y + alto / 2)
        print("Centro en x=", cx, "centro en y=", cy)

        a2 = cv.pointPolygonTest(pts, (cx, cy), False)
        print("a2: ", a2)

        if a2 >= 0:
            cv.circle(frame, (cx, cy), 3, (247, 17, 130), -1)


    # Muestra el video
    if frame is not None:
        cv.imshow("Video", frame)
        # cv.imshow("Filtro", cierre)
    else:
        break

    key = cv.waitKey(int(1000 / fps))  # Esperar 1 milisegundo

    if key == ord('q'):  # Presionar 'q' para salir del bucle
        break

    time.sleep(2)


# Liberar la cámara
cap.release()

# Cerrar todas las ventanas
cv.destroyAllWindows()
