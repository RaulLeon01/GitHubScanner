# INSTALACIÓN DE FLASK:
# 1. cd C:/Users/TuUsuario/Documents/Flask_
# 2. python -m venv venv
# 3. venv/Scripts/activate
# 4. pip install flask
# 5. pip show flask
# 6. python app.py


from flask import Flask, jsonify, request
import random
import string

app = Flask(__name__)

# --- DICCIONARIO ORIGINAL DE DISPOSITIVOS ---
dispositivos_data = {
    "dispositivos": [
        { "Router1": { "ID": "1", "IP": "192.168.0.1", "MAC": "00:1A:2B:3C:4D:01", "Lvl": 3 } },
        { "Switch1": { "ID": "2", "IP": "192.168.0.2", "MAC": "00:1A:2B:3C:4D:02", "Lvl": 2 } },
        { "PC1": { "ID": "3", "IP": "192.168.0.10", "MAC": "00:1A:2B:3C:4D:03", "Lvl": 1 } }
    ]
}

# --- FUNCIÓN AUXILIAR PARA CREAR ID ALEATORIO ---
def generar_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))  # ej: 'A9K4T2'

# --- 1️⃣ AGREGAR NUEVO DISPOSITIVO ---
@app.route('/agregar', methods=['POST'])
def agregar_dispositivo():
    data = request.get_json()

    nombre = data.get("nombre")
    ip = data.get("IP")
    mac = data.get("MAC")
    lvl = data.get("Lvl")

    if not nombre or not ip or not mac or lvl is None:
        return jsonify({"error": "Faltan datos"}), 400

    nuevo_id = generar_id()
    nuevo_dispositivo = {nombre: {"ID": nuevo_id, "IP": ip, "MAC": mac, "Lvl": lvl}}
    dispositivos_data["dispositivos"].append(nuevo_dispositivo)

    return jsonify({"mensaje": "Dispositivo agregado correctamente", "dispositivo": nuevo_dispositivo}), 201


# --- 2️⃣ ELIMINAR DISPOSITIVO POR NOMBRE ---
@app.route('/eliminar/<nombre>', methods=['DELETE'])
def eliminar_dispositivo(nombre):
    for dispositivo in dispositivos_data["dispositivos"]:
        if nombre in dispositivo:
            dispositivos_data["dispositivos"].remove(dispositivo)
            return jsonify({"mensaje": f"Dispositivo '{nombre}' eliminado correctamente"}), 200

    return jsonify({"error": f"Dispositivo '{nombre}' no encontrado"}), 404


# --- 3️⃣ MODIFICAR INFORMACIÓN DE UN DISPOSITIVO ---
@app.route('/modificar/<nombre>', methods=['PUT'])
def modificar_dispositivo(nombre):
    data = request.get_json()

    for dispositivo in dispositivos_data["dispositivos"]:
        if nombre in dispositivo:
            if "IP" in data:
                dispositivo[nombre]["IP"] = data["IP"]
            if "MAC" in data:
                dispositivo[nombre]["MAC"] = data["MAC"]
            if "Lvl" in data:
                dispositivo[nombre]["Lvl"] = data["Lvl"]
            return jsonify({"mensaje": f"Dispositivo '{nombre}' modificado correctamente", "nuevo": dispositivo}), 200

    return jsonify({"error": f"Dispositivo '{nombre}' no encontrado"}), 404


# --- LISTAR TODOS LOS DISPOSITIVOS ---
@app.route('/listar', methods=['GET'])
def listar_dispositivos():
    return jsonify(dispositivos_data), 200


# --- EJECUTAR SERVIDOR ---
if __name__ == '__main__':
    app.run(debug=True)