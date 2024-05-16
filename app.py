from flask import Flask, render_template, request
import sqlite3
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
