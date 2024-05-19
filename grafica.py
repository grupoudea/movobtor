import matplotlib.pyplot as plt

def generar_grafica_distancia_x_tiempo(vector_velocidad):
    data = vector_velocidad

    tiempo_inicial = []
    tiempo_final = []
    distancia_inicial = []
    distancia_final = []
    velocidad_instantanea = []

    # Extrae los valores de la tupla
    for _, tupla in data.items():
        tiempo_inicial.append(tupla[0])
        tiempo_final.append(tupla[1])
        distancia_inicial.append(tupla[2])
        distancia_final.append(tupla[3])
        velocidad_instantanea.append(tupla[5])

    plt.figure(figsize=(12, 6))
    plt.plot(tiempo_inicial, distancia_inicial, 'o-', label="Distancia Inicial")
    plt.plot(tiempo_final, distancia_final, 'x-', label="Distancia Final")
    plt.xlabel("Tiempo")
    plt.ylabel("Distancia")
    plt.title("Gráfica de Distancia vs tiempo")


    for i, key in enumerate(data.keys()):
        # plt.annotate(f"{distancia_inicial[i]:.2f}", (tiempo_inicial[i], distancia_inicial[i]), textcoords="offset points", xytext=(0,10), ha='center')
        plt.annotate(f"{velocidad_instantanea[i]:.2f}", (tiempo_final[i], distancia_final[i]),
                     textcoords="offset points",
                     xytext=(0, 10), ha='center')
        # plt.annotate(f"ID: {key}\nTiempo: {tiempo_final[i]:.2f}\nDistancia: {distancia_final[i]:.2f}", (tiempo_final[i], distancia_final[i]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.legend()
    plt.grid(True)
    plt.show()


def generar_grafica_velocidad_x_tiempo(vector_velocidad):
    data = vector_velocidad

    tiempo_inicial = []
    tiempo_final = []
    velocidad_inicial = []
    velocidad_final = []
    aceleracion = []

    # Extrae los valores de la tupla
    for _, tupla in data.items():
        tiempo_inicial.append(tupla[0])
        tiempo_final.append(tupla[1])
        velocidad_inicial.append(tupla[4])
        velocidad_final.append(tupla[5])
        aceleracion.append(tupla[6])

    plt.figure(figsize=(12, 6))
    plt.plot(tiempo_inicial, velocidad_inicial, 'o-', label="Velocidad Inicial")
    plt.plot(tiempo_final, velocidad_final, 'x-', label="Velocidad Final")
    plt.xlabel("Tiempo")
    plt.ylabel("Velocidad")
    plt.title("Gráfica de Velocidad vs Tiempo ")


    for i, key in enumerate(data.keys()):
        # plt.annotate(f"{distancia_inicial[i]:.2f}", (tiempo_inicial[i], distancia_inicial[i]), textcoords="offset points", xytext=(0,10), ha='center')
        plt.annotate(f"{aceleracion[i]:.2f}", (tiempo_final[i], velocidad_final[i]),
                     textcoords="offset points",
                     xytext=(0, 10), ha='center')
        # plt.annotate(f"ID: {key}\nTiempo: {tiempo_final[i]:.2f}\nDistancia: {distancia_final[i]:.2f}", (tiempo_final[i], distancia_final[i]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.legend()
    plt.grid(True)
    plt.show()

