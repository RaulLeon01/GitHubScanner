# -*- coding: utf-8 -*-

# INSTALACIÓN DE FLASK (Instrucciones para configurar el entorno)
# 1. cd C:/Users/TuUsuario/Documents/Flask_  --> Navegar a la carpeta de tu proyecto.
# 2. python -m venv venv                     --> Crear un entorno virtual llamado 'venv'.
# 3. venv\Scripts\activate.bat               --> Activar el entorno virtual.
# 4. pip install flask                       --> Instalar la librería Flask.
# 5. pip show flask                          --> Verificar que Flask se instaló correctamente.
# 6. python app.py                           --> Ejecutar esta aplicación.

# --- PRIMERA PARTE DEL CRUD (Create, Read, Update, Delete) ---
# Este código se enfoca en la parte de "Read" (Leer/Consultar).

# Importamos las clases necesarias de la librería Flask.
# Flask: Es la clase principal para crear la aplicación.
# jsonify: Convierte los diccionarios de Python a formato JSON, el estándar para las APIs.
# request: Permite acceder a la información de la solicitud entrante (como los parámetros de la URL).
from flask import Flask, jsonify, request

# Creamos una instancia de la aplicación Flask.
# '__name__' es una variable especial de Python que ayuda a Flask a saber dónde buscar recursos.
app = Flask(__name__)

# DICCIONARIO DE DISPOSITIVOS
# Esta es nuestra "base de datos" simulada. Es un diccionario de Python
# donde cada clave (ej. "Router01") tiene como valor otro diccionario con sus detalles.
devices_info = {
    "Router01": {
        "ios": "IOS-XE 17.3",
        "mac": "00:1A:2B:3C:4D:5E",
        "services": ["SSH", "SNMP", "HTTP"],
        "description": "Router principal en el centro de datos"
    },
    "Switch02": {
        "ios": "IOS 15.2",
        "mac": "00:1B:2C:3D:4E:5F",
        "services": ["Telnet", "SNMP"],
        "description": "Switch de acceso en el edificio A"
    },
    "Firewall01": {
        "ios": "ASA 9.8",
        "mac": "00:1C:2D:3E:4F:5A",
        "services": ["VPN", "SSH"],
        "description": "Firewall perimetral"
    }
}

# --- ENDPOINT PARA OBTENER UN DISPOSITIVO ESPECÍFICO ---
# @app.route define la URL para esta función.
# methods=['GET'] especifica que esta ruta solo responde a solicitudes de tipo GET (consulta).
@app.route('/device', methods=['GET'])
def get_device_info():
    
    # Obtenemos el valor del parámetro 'name' de la URL.
    # Ejemplo: si la URL es /device?name=Router01, device_name será "Router01".
    device_name = request.args.get('name')

    # PRIMER NIVEL DE VALIDACIÓN: ¿Nos dieron un nombre para buscar?
    if not device_name:
        # Si no se proporciona el parámetro 'name', devolvemos un error 400 (Bad Request).
        return jsonify({"error": "Debes proporcionar el parámetro 'name'"}), 400

    # SEGUNDO NIVEL DE VALIDACIÓN: ¿El dispositivo que buscan existe?
    # Usamos .get() para buscar en el diccionario. Devuelve None si la clave no existe.
    device = devices_info.get(device_name)
    if not device:
        # Si el dispositivo no está en nuestro diccionario, devolvemos un error 404 (Not Found).
        return jsonify({"error": f"Dispositivo '{device_name}' no encontrado"}), 404
    
    # Si todo salió bien, devolvemos la información del dispositivo en formato JSON.
    return jsonify({device_name: device})

# --- ENDPOINT PARA OBTENER TODOS LOS DISPOSITIVOS ---
# Esta es la ruta que se usará para obtener la lista completa.
@app.route('/devices', methods=['GET'])
def get_all_devices():
    # Simplemente convertimos todo el diccionario devices_info a JSON y lo devolvemos.
    return jsonify(devices_info)

# Esta sección de código está comentada, por lo que no se ejecuta.
# Era un ejemplo simple para mostrar cómo recibir un parámetro y mostrarlo en HTML.
"""
@app.route('/', methods=['GET'])
def decir_hola():
    dato_entrada = request.args.get('dato1')
    return "<h1>Dato: "+dato_entrada+ "</h1>"
"""

# Esta condición asegura que el servidor de desarrollo solo se ejecute
# cuando el script se llama directamente (no cuando es importado por otro script).
if __name__ == '__main__':
    # app.run() inicia el servidor web.
    # debug=True activa el modo de depuración, que reinicia el servidor
    # automáticamente cuando haces cambios en el código y muestra errores detallados.
    app.run(debug=True)