import matplotlib.pyplot as plt

# Tu tupla de datos
data = {3: (0, 0.061007022857666016, 0, 39, 639.2706638216052),
        4: (0.061007022857666016, 0.1250002384185791, 39, 127, 1375.145774886646),
        5: (0.1250002384185791, 0.18783974647521973, 127, 211, 1336.7386632671644),
        6: (0.18783974647521973, 0.25000548362731934, 211, 287, 1222.5383866043828),
        7: (0.25000548362731934, 0.31419944763183594, 287, 363, 1183.911932820549),
        8: (0.31419944763183594, 0.3779323101043701, 363, 436, 1145.4059517797355),
        9: (0.3779323101043701, 0.4363570213317871, 436, 499, 1078.310849578251),
        10: (0.4363570213317871, 0.49855542182922363, 499, 560, 980.7326155037392),
        11: (0.49855542182922363, 0.560765266418457, 560, 621, 980.5522004238734),
        12: (0.560765266418457, 0.6229045391082764, 621, 681, 965.5729364503838),
        13: (0.6229045391082764, 0.6844863891601562, 681, 734, 860.643192033853),
        14: (0.6844863891601562, 0.7471926212310791, 734, 788, 861.158424236433),
        15: (0.7471926212310791, 0.8112292289733887, 788, 846, 905.731924985759),
        16: (0.8112292289733887, 0.8740706443786621, 846, 899, 843.3928430509607),
        17: (0.8740706443786621, 0.9358348846435547, 899, 947, 777.1487157316122)}

# Inicializa listas para almacenar los valores de tiempo y distancia
tiempo_inicial = []
tiempo_final = []
distancia_inicial = []
distancia_final = []
velocidad_instantanea = []

# Extrae los valores de la tupla y los agrega a las listas correspondientes
for _, tupla in data.items():
    tiempo_inicial.append(tupla[0])
    tiempo_final.append(tupla[1])
    distancia_inicial.append(tupla[2])
    distancia_final.append(tupla[3])
    velocidad_instantanea.append(tupla[4])

# Grafica los datos
plt.figure(figsize=(12, 6))
plt.plot(tiempo_inicial, distancia_inicial, 'o-', label="Distancia Inicial")
plt.plot(tiempo_final, distancia_final, 'x-', label="Distancia Final")
plt.xlabel("Tiempo")
plt.ylabel("Distancia")
plt.title("Gráfica de Tiempo vs Distancia")

# Agrega etiquetas a los puntos de datos
for i, key in enumerate(data.keys()):
    # plt.annotate(f"{distancia_inicial[i]:.2f}", (tiempo_inicial[i], distancia_inicial[i]), textcoords="offset points", xytext=(0,10), ha='center')
    plt.annotate(f"{velocidad_instantanea[i]:.2f}", (tiempo_final[i], distancia_final[i]), textcoords="offset points", xytext=(0,10), ha='center')
    # plt.annotate(f"ID: {key}\nTiempo: {tiempo_final[i]:.2f}\nDistancia: {distancia_final[i]:.2f}", (tiempo_final[i], distancia_final[i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.legend()
plt.grid(True)
plt.show()