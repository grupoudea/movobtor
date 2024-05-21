import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from detececcion_velocidad import iniciar_procesamiento


def select_video():
    filepath = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4;*.avi;*.mkv;*.mov;*.flv")]
    )
    if filepath:
        video_path_entry.config(state='normal')
        video_path_entry.delete(0, tk.END)
        video_path_entry.insert(0, filepath)
        video_path_entry.config(state='readonly')


def show_info():
    video_path = video_path_entry.get()
    distance = distance_entry.get()

    if not video_path:
        messagebox.showerror("Error", "Por favor, seleccione un video.")
    elif not distance:
        messagebox.showerror("Error", "Por favor, ingrese la distancia.")
    else:
        try:
            distance_value = float(distance)
            process_video(video_path, distance_value)
        except ValueError:
            messagebox.showerror("Error", "La distancia debe ser un número.")


def process_video(video_path, distance):
    print(f"Video: {video_path}")
    print(f"Distancia: {distance}")
    tiempo, velocidad = iniciar_procesamiento(video_path, distance)

    speed = velocidad
    time = tiempo
    speed_var.set("Velocidad: {:.3f} m/s".format(speed))
    time_var.set("Tiempo: {:.3f} s".format(time))
    result_var.set(
        f"El objeto se mueve a {speed:.3f} cm/s, en una distancia de {distance_entry.get()} cm, en {time:.3f} s")


def exit_app():
    root.quit()


# Ventana principal
root = tk.Tk()
root.title("Seleccionar Video")
root.resizable(False, False)
root.configure(bg='#001f3f')

# Centrar la ventana en la pantalla
window_width = 400
window_height = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Estilo para botones y etiquetas
title_font = ("Helvetica", 20, "bold")
button_font = ("Helvetica", 12)
label_font = ("Helvetica", 12)
label_small_font = ("Helvetica", 9)
entry_font = ("Helvetica", 11)
label_bold_font = ("Helvetica", 11, "bold")

title = tk.Label(root, text="Movobtor", font=title_font, fg="white", bg="#001f3f")
title.pack(pady=5)

info_label = tk.Label(root,
                      text="El video debe tener las siguientes características: "
                           "\n- Fondo sólido"
                           "\n- Cámara estática"
                           "\n- Buena iluminación"
                           "\n- El objeto debe entrar y salir de la visualización del video",
                      wraplength=380, font=label_small_font, justify="left", fg="white", bg="#001f3f")
info_label.pack(pady=10, padx=10, anchor="w")

# Seleccionar el video
video_label = tk.Label(root, text="Seleccionar video:", wraplength=380, font=label_bold_font, justify="left",
                       fg="white", bg="#001f3f")
video_label.pack(pady=5, padx=10, anchor="w")
select_video_button = tk.Button(root, text="Seleccionar", command=select_video, font=button_font, fg="white",
                                bg="#0056b3")
select_video_button.pack(pady=10, padx=10, anchor="w")

# Ruta del video
video_path_entry = tk.Entry(root, width=50, font=entry_font)
video_path_entry.pack(pady=5, padx=10, anchor="w")

# Distancia
distance_label = tk.Label(root, text="Distancia (cm):", wraplength=380, font=label_bold_font, justify="left",
                          fg="white", bg="#001f3f")
distance_label.pack(pady=5, padx=10, anchor="w")
distance_entry = tk.Entry(root, width=50, font=entry_font)
distance_entry.pack(pady=5, padx=10, anchor="w")

# Boton ejecutar
show_info_button = tk.Button(root, text="Procesar video", command=show_info, font=button_font, fg="white", bg="#0056b3")
show_info_button.pack(pady=10, padx=10, anchor="w")

# Velocidad
speed_var = tk.StringVar()
speed_label = tk.Label(root, textvariable=speed_var, font=label_bold_font, fg="white", bg="#001f3f")
speed_label.pack(pady=3, padx=10, anchor="w")

time_var = tk.StringVar()
time_label = tk.Label(root, textvariable=time_var, font=label_bold_font, fg="white", bg="#001f3f")
time_label.pack(pady=3, padx=10, anchor="w")

result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, font=label_font, wraplength=380, justify="left", fg="white",
                        bg="#001f3f")
result_label.pack(pady=3, padx=10, anchor="w")

# Bucle principal de la ventana
root.mainloop()
