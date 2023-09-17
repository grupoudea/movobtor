import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

# Variables globales
pausar_video = False
mostrar_pixel = False
x, y = -1, -1

# Función de callback de mouse
def mouse_callback(event, _x, _y, flags, param):
    global pausar_video, mostrar_pixel, x, y

    if event == cv2.EVENT_LBUTTONDOWN:
        x, y = _x, _y
        mostrar_pixel = True
    if event == cv2.EVENT_RBUTTONDOWN:
        pausar_video = not pausar_video

# Cargar el video
video_path = 'video1-horizontal.mp4'  # Cambia esto al camino de tu video
cap = cv2.VideoCapture(video_path)

# Obtener las dimensiones del video
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

print("frame w: ", frame_width)
print("frame h: ", frame_height)

# Crear una ventana y configurar la función de callback de mouse
cv2.namedWindow('Video')
cv2.setMouseCallback('Video', mouse_callback)

# Cambiar el tamaño de la ventana al tamaño del video
cv2.resizeWindow('Video', frame_width, frame_height)

while True:
    if not pausar_video:
        ret, frame = cap.read()

        if not ret:
            # El video ha terminado, reiniciar la reproducción
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue  # Continuar desde el principio

        frame2 = np.copy(frame)

    if mostrar_pixel:
        pixel_color = frame[y, x]  # Obtener el valor del color en (x, y)
        frame2 = np.copy(frame)
        cv2.putText(frame2, f'Posición (x, y): ({x}, {y}) Color: {pixel_color}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Video', frame2)

    key = cv2.waitKey(1)  # Esperar 1 milisegundo

    if key == ord('q'):  # Presionar 'q' para salir del bucle
        break

# Liberar la cámara
cap.release()

# Cerrar todas las ventanas
cv2.destroyAllWindows()
