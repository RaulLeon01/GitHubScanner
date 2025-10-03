
# INSTALACIÓN DE FLASK:
# 1. cd C:/Users/TuUsuario/Documents/Flask_
# 2. python -m venv venv
# 3. ven\Scripts\activate.bat
# 4. pip install flask
# 5. pip show flask
# 6. python app.py

# PRIMER PARTE DEL CRUD

from flask import Flask, jsonify, request

app = Flask(__name__)

#DICCIONARIO DE DISPOSITIVOS
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

# ESTA ES LA RUTA QUE OPCUPAREMOS PARA 1 DESP. EN POSTMAN (OJO CON LOS PARÁMETROS)
@app.route('/device', methods=['GET'])
def get_device_info():

    #CONSIDERA EN TODAS LAS LLAMDAS A API's UNA FORMA DE PREVENIR ERRORES
    device_name = request.args.get('name')
    if not device_name:
        return jsonify({"error": "Debes proporcionar el parámetro 'name'"}), 400

    #CONSIDERA EN TODAS LAS LLAMDAS A API's UNA FORMA DE PREVENIR ERRORES x2
    device = devices_info.get(device_name)
    if not device:
        return jsonify({"error": f"Dispositivo '{device_name}' no encontrado"}), 404
    
    #PUEDES VERIFICAR LOS DIFERENTES TIPOS DE ERROR 400 & 404

    return jsonify({device_name: device})

# ESTA ES LA RUTA QUE OPCUPAREMOS EN POSTMAN (TODOS LOS DISP.)
@app.route('/devices', methods=['GET'])
def get_all_devices():
    return jsonify(devices_info)

"""
@app.route('/', methods=['GET'])
def decir_hola():
    dato_entrada = request.args.get('dato1')
    return "<h1>Dato: "+dato_entrada+ "</h1>"
"""

if __name__ == '__main__':
    app.run(debug=True)