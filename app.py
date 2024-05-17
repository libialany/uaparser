from flask import Flask, render_template, request
import sqlite3
import requests
from enum import Enum
import os
from dotenv import load_dotenv
load_dotenv()
class Status(Enum):
    SUCCESS = 1
    FAIL = 2
app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/status-client', methods=['POST'])
def statusClient():
    data = request.get_json()
    visitor_id = data.get('visitorId')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO dispositivos (visitante, ultimoping) VALUES (?, datetime('now'))", (visitor_id,))
    conn.commit()
    conn.close()
    return str(visitor_id)

""" description: Counts all pings received on 10 minutes"""
@app.route('/usuariosactivos')
def pingcount():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) as count FROM dispositivos WHERE ultimoping >= datetime('now', '-10 seconds')")
    count = cursor.fetchone()
    conn.close()
    return str(count['count'])

""" 
    Obtener una lista de IPs en blacklist.
    output: str 
"""
@app.route('/blacklist')
def blacklist():
    ip = request.remote_addr
    url = os.getenv('URL_BLACKLIST')
    response = requests.get(url)
    ips_contaminadas = response.text 
    if ip in ips_contaminadas:
        return Status.FAIL
    else:
        return Status.SUCCESS

""" 
    Checks the browser and 'version' attributes.
    input: [str, str]
    ouput: str
"""
@app.route('/navegador_actual', methods=['GET', 'POST'])
def navegador():
    navegador = request.args.get('navegador')
    version = request.args.get('version')
    try:
        version = int(version)
    except ValueError:
        return Status.FAIL
    min_versions = {
        'Chrome': 121,
        'Firefox': 120,
    } 
    if navegador in min_versions and version > min_versions[version]:
        return Status.SUCCESS
    elif navegador == 'Opera' and int(version) >= 700:
        return Status.SUCCESS
    else:
        return  Status.FAIL
""" 
    Checks the device and 'version' attributes.
    input: [str, str]
    ouput: str
"""
@app.route('/os_actual', methods=['GET', 'POST'])
def os():
    os = request.args.get('os')
    version = request.args.get('version')
    try:
        version = int(version)
    except ValueError:
        return Status.FAIL
    min_versions = {
        'Android': 10,
        'iOS': 14,
        'Windows': 11,
        'Mac': 11
    } 
    if os in min_versions and version >= min_versions[os]:
        return Status.SUCCESS
    elif os == 'Linux':
        return Status.SUCCESS
    else:
        return Status.FAIL

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
