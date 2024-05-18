import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


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


def exit_app():
    root.quit()


# Ventana principal
root = tk.Tk()
root.title("Seleccionar Video")
root.geometry("400x300")

info_label = tk.Label(root,
                      text="El video debe tener las siguientes características:"
                           "\n- Fondo sólido"
                           "\n- Cámara estática"
                           "\n- Buena iluminación"
                           "\n- El objeto debe entrar y salir de la visualización del video",
                      wraplength=380)
info_label.pack(pady=10)

# Seleccionar el video
select_video_button = tk.Button(root, text="Seleccionar video", command=select_video)
select_video_button.pack(pady=10)


# Ruta del video
video_path_entry = tk.Entry(root, width=50)
video_path_entry.pack(pady=5)

# Distancia
distance_label = tk.Label(root, text="Distancia (m):")
distance_label.pack(pady=5)
distance_entry = tk.Entry(root)
distance_entry.pack(pady=5)

# Boton ejecutar
show_info_button = tk.Button(root, text="Procesar video", command=show_info)
show_info_button.pack(pady=20)

# Bucle principal de la ventana
root.mainloop()
