import numpy as np
import cv2 as cv

cap = cv.VideoCapture("videoPunto2-horizontal1.mp4")
deteccion = cv.createBackgroundSubtractorMOG2(history=10000, varThreshold=100)


# 90,0   90, 720
# 1094,0   1094,720


while True:
    ret, frame = cap.read()

    if frame is not None:
        height, width = frame.shape[:2]
        print("height" ,height)
        print("width", width)

    if not ret:
        # El video ha terminado, reiniciar la reproducción
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        continue  # Continuar desde el principio

    mask = np.zeros((height, width), dtype=np.uint8)

    # Definir los puntos para el cuadro
    pts = np.array([[90, 0], [90, 720], [1094, 720], [1094, 0]], np.int32)
    pts = pts.reshape((-1, 1, 2))

    # Dibujar el cuadro
    cv.polylines(frame, [pts], isClosed=True, color=(255, 0,0), thickness=2)

    # muestra el video
    cv.imshow("Video", frame)

    key = cv.waitKey(1)  # Esperar 1 milisegundo

    if key == ord('q'):  # Presionar 'q' para salir del bucle
        break

# Liberar la cámara
cap.release()

# Cerrar todas las ventanas
cv.destroyAllWindows()


