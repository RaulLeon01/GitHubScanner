# INSTALACIÓN DE FLASK:
# 1. cd C:/Users/TuUsuario/Documents/Flask_
# 2. python -m venv venv
# 3. venv/Scripts/activate
# 4. pip install flask
# 5. pip show flask
# 6. python app.py

from flask import Flask, jsonify, request
import json
import random
import string
import os

app = Flask(__name__)

# Ruta del archivo JSON
JSON_PATH = "archivo.json"

# --------------------------------------------------------
# Función auxiliar para cargar y guardar el archivo JSON
# --------------------------------------------------------
def cargar_json():
    if not os.path.exists(JSON_PATH):
        return {"dispositivos": []}
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def guardar_json(data):
    with open(JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

# --------------------------------------------------------
# Agregar un nuevo dispositivo con ID alfanumérico random
# --------------------------------------------------------
@app.route('/agregar', methods=['POST'])
def agregar_dispositivo():
    data = cargar_json()
    dispositivos = data["dispositivos"]

    nuevo_dispositivo = request.json  # Ejemplo: {"nombre": "PC9", "IP": "192.168.5.10", "MAC": "00:1A:2B:3C:4D:2A", "Lvl": 1}

    if not nuevo_dispositivo or "nombre" not in nuevo_dispositivo:
        return jsonify({"error": "Debes enviar al menos el nombre del dispositivo."}), 400

    nombre = nuevo_dispositivo["nombre"]

    # ID alfanumérico random de 6 caracteres
    id_random = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # Crear el nuevo registro
    nuevo = {
        nombre: {
            "ID": id_random,
            "IP": nuevo_dispositivo.get("IP", "0.0.0.0"),
            "MAC": nuevo_dispositivo.get("MAC", "00:00:00:00:00:00"),
            "Lvl": nuevo_dispositivo.get("Lvl", 1)
        }
    }

    dispositivos.append(nuevo)
    guardar_json(data)

    return jsonify({"mensaje": "Dispositivo agregado exitosamente", "dispositivo": nuevo}), 201


# --------------------------------------------------------
# Borrar un dispositivo por nombre
# --------------------------------------------------------
@app.route('/eliminar/<nombre>', methods=['DELETE'])
def eliminar_dispositivo(nombre):
    data = cargar_json()
    dispositivos = data["dispositivos"]

    # Buscar y eliminar por nombre
    eliminado = False
    for dispositivo in dispositivos:
        if nombre in dispositivo:
            dispositivos.remove(dispositivo)
            eliminado = True
            break

    if not eliminado:
        return jsonify({"error": f"No se encontró el dispositivo '{nombre}'"}), 404

    guardar_json(data)
    return jsonify({"mensaje": f"Dispositivo '{nombre}' eliminado correctamente."})


# --------------------------------------------------------
# Modificar información de un dispositivo existente
# --------------------------------------------------------
@app.route('/modificar/<nombre>', methods=['PUT'])
def modificar_dispositivo(nombre):
    data = cargar_json()
    dispositivos = data["dispositivos"]
    cambios = request.json  # Ejemplo: {"IP": "192.168.5.5", "Lvl": 2}

    for dispositivo in dispositivos:
        if nombre in dispositivo:
            # Actualiza los campos enviados
            for clave, valor in cambios.items():
                if clave in dispositivo[nombre]:
                    dispositivo[nombre][clave] = valor
            guardar_json(data)
            return jsonify({"mensaje": f"Dispositivo '{nombre}' actualizado correctamente.", "nuevo_valor": dispositivo[nombre]})

    return jsonify({"error": f"No se encontró el dispositivo '{nombre}'"}), 404


# --------------------------------------------------------
# (Opcional) Ver todos los dispositivos
# --------------------------------------------------------
@app.route('/dispositivos', methods=['GET'])
def listar_dispositivos():
    data = cargar_json()
    return jsonify(data)


# --------------------------------------------------------
# Ejecutar servidor Flask
# --------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)