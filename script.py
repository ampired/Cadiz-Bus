import paho.mqtt.client as mqtt
import json
import time
import random

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "reto_telefonica/cadiz/flota_global"

# Coordenadas de puntos por los que pasa cada Línea de Cádiz
waypoints = {
    "L1": [(36.5350, -6.2940), (36.5320, -6.2920), (36.5260, -6.2890), (36.5220, -6.2840), (36.5180, -6.2800), (36.5120, -6.2770), (36.5080, -6.2750), (36.5020, -6.2720), (36.4940, -6.2680)],
    "L2": [(36.5350, -6.2940), (36.5320, -6.2920), (36.5260, -6.2890), (36.5200, -6.2810), (36.5140, -6.2740), (36.5060, -6.2680)],
    "L3": [(36.5350, -6.2940), (36.5320, -6.2920), (36.5260, -6.2890), (36.5200, -6.2810), (36.5140, -6.2740), (36.5050, -6.2620)],
    "L5": [(36.5350, -6.2940), (36.5320, -6.2920), (36.5260, -6.2890), (36.5200, -6.2810), (36.5140, -6.2730), (36.5040, -6.2650), (36.4950, -6.2600)],
    "L7": [(36.5070, -6.2780), (36.5120, -6.2800), (36.5180, -6.2820), (36.5220, -6.2840), (36.5260, -6.2890), (36.5290, -6.2940), (36.5310, -6.2980), (36.5300, -6.3040)]
}

nombres_sentidos = {
    "L1": ["Hacia P. España", "Hacia Cortadura"],
    "L2": ["Hacia P. España", "Hacia Bda. Loreto"],
    "L3": ["Hacia P. España", "Hacia Puntales"],
    "L5": ["Hacia P. España", "Hacia Zona Franca"],
    "L7": ["Hacia Gta. Ana Orantes", "Hacia La Caleta"]
}

def calcular_ruta(p1, p2, num_pasos):
    return [(p1[0] + (p2[0] - p1[0]) * (i / num_pasos), p1[1] + (p2[1] - p1[1]) * (i / num_pasos)) for i in range(num_pasos)]

rutas_completas = {}
for linea, puntos in waypoints.items():
    ruta = []
    for i in range(len(puntos) - 1):
        ruta.extend(calcular_ruta(puntos[i], puntos[i+1], 15)) # 15 pasos entre cada micro-punto
    rutas_completas[linea] = ruta

flota = []
for linea in waypoints.keys():
    longitud = len(rutas_completas[linea])
    flota.append({"id": f"BUS-{linea}-01", "linea": linea, "idx": 0, "dir": 1, "bat": random.randint(70, 100)})
    flota.append({"id": f"BUS-{linea}-02", "linea": linea, "idx": longitud//2, "dir": -1, "bat": random.randint(40, 90)})
    flota.append({"id": f"BUS-{linea}-03", "linea": linea, "idx": longitud-2, "dir": -1, "bat": random.randint(15, 60)})

cliente = mqtt.Client()
cliente.connect(BROKER, PORT, 60)
print("Conectado al broker MQTT")

while True:
    for bus in flota:
        ruta = rutas_completas[bus["linea"]]
        
        bus["idx"] += bus["dir"]
        if bus["idx"] >= len(ruta) - 1: bus["dir"] = -1
        elif bus["idx"] <= 0: bus["dir"] = 1
            
        sentido_texto = nombres_sentidos[bus["linea"]][1] if bus["dir"] == 1 else nombres_sentidos[bus["linea"]][0]

        lat = ruta[bus["idx"]][0] + random.uniform(-0.00005, 0.00005)
        lng = ruta[bus["idx"]][1] + random.uniform(-0.00005, 0.00005)

        bus["bat"] -= random.choice([0, 0.2])
        if bus["bat"] < 0: bus["bat"] = 100 

        ia_ret = random.random() < 0.05
        causa = random.choice(["Tráfico denso en Avenida", "Lluvia intensa", "Accidente en vía"]) if ia_ret else ""

        payload = {
            "id": bus["id"], "linea": bus["linea"],
            "lat": round(lat, 5), "lng": round(lng, 5),
            "bateria": round(bus["bat"], 1), "sentido": sentido_texto,
            "ia_bat": bus["bat"] < 20, "ia_ret": ia_ret, "causa_ret": causa
        }
        cliente.publish(TOPIC, json.dumps(payload))
        
    print("Telemetría enviada...")
    time.sleep(2)