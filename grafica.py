import matplotlib.pyplot as plt

# Tu tupla de datos
data = {3: (0, 0.059731483459472656, 0, 2.7421875, 45.908578544856546), 4: (0.059731483459472656, 0.1267256736755371, 2.7421875, 8.9296875, 92.35875499120978), 5: (0.1267256736755371, 0.19272828102111816, 8.9296875, 14.8359375, 89.48510123358679), 6: (0.19272828102111816, 0.25373172760009766, 14.8359375, 20.1796875, 87.59750964368207), 7: (0.25373172760009766, 0.31372761726379395, 20.1796875, 25.5234375, 89.06860169845136), 8: (0.31372761726379395, 0.3747282028198242, 25.5234375, 30.65625, 84.14365949463563), 9: (0.3747282028198242, 0.4377264976501465, 30.65625, 35.0859375, 70.314403142669), 10: (0.4377264976501465, 0.499727725982666, 35.0859375, 39.375, 69.17705689631305), 11: (0.499727725982666, 0.5627260208129883, 39.375, 43.6640625, 68.08219986829856), 12: (0.5627260208129883, 0.6227278709411621, 43.6640625, 47.8828125, 70.3103319478992), 13: (0.6227278709411621, 0.6837248802185059, 47.8828125, 51.609375, 61.09418386491557), 14: (0.6837248802185059, 0.7468841075897217, 51.609375, 55.40625, 60.115919051447854), 15: (0.7468841075897217, 0.8080523014068604, 55.40625, 59.484375, 66.67067875490143), 16: (0.8080523014068604, 0.8712975978851318, 59.484375, 63.2109375, 58.92236589135598), 17: (0.8712975978851318, 0.9316713809967041, 63.2109375, 66.5859375, 55.90174784579782)}

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