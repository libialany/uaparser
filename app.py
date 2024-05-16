from flask import Flask, render_template, request
import sqlite3
import requests
# from ua_parser import parse_user_agent
app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def hello_world():
    return render_template('index.html')


# Este endpoint recibe los pings de los clientes
# y guardamos el último ping en la base de datos
@app.route('/estoyvivo', methods=['POST'])
def estoyvivo():
    data = request.get_json()
    visitor_id = data.get('visitorId')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO dispositivos (visitante, ultimoping) VALUES (?, datetime('now'))", (visitor_id,))
    conn.commit()
    conn.close()
    return str(visitor_id)

# This Flask endpoint counts all pings received on 10 minutes
@app.route('/usuariosactivos')
def pingcount():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) as count FROM dispositivos WHERE ultimoping >= datetime('now', '-10 minutes')")
    count = cursor.fetchone()
    conn.close()
    return str(count['count'])

# Obtener una lista de IPs en blacklist.
# Si la IP del cliente está presente, responder con NOK en json.
# De lo contrario, con OK.
@app.route('/blacklist', methods=['GET', 'POST'])
def blacklist():
    ip = request.remote_addr
    url = 'http://192.168.210.1:3080/cgi-bin/dominios.sh'
    response = requests.get(url)
    ips_contaminadas = response.text 
    if ip in ips_contaminadas:
        return 'NOK'
    else:
        return 'OK'

# Verificar el atributo "navegador" y "version". Si el navegador es Chrome y la versión es mayor a 80, responder con OK.
# De lo contrario, responder con NOK.
@app.route('/navegador_actual', methods=['GET', 'POST'])
def navegador():
    navegador = request.args.get('navegador')
    version = request.args.get('version')
    if navegador == 'Chrome' and int(version) > 121:
        return "OK";
    elif navegador == 'Firefox' and int(version) > 120:
        return "OK";
    elif navegador == 'Opera' and int(version) >= 700:
        return "OK";
    else:
        return "NOK";

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
