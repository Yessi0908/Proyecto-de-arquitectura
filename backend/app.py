import os
import time
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pymysql
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')
DB_NAME = os.environ.get('DB_NAME', 'invernadero')

def get_conn():
    # retry loop waiting for DB
    for i in range(10):
        try:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, cursorclass=pymysql.cursors.DictCursor)
            return conn
        except Exception as e:
            print(f"DB not ready yet ({i}): {e}")
            time.sleep(2)
    raise RuntimeError('Cannot connect to DB')

@app.route('/api/init', methods=['POST'])
def init_db():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS registros_ambiente (
              id INT AUTO_INCREMENT PRIMARY KEY,
              fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
              temperatura FLOAT,
              humedad FLOAT,
              estado_bomba VARCHAR(15),
              alerta VARCHAR(50)
            );
            ''')
            cur.execute('''
            CREATE TABLE IF NOT EXISTS registros_seguridad (
              id INT AUTO_INCREMENT PRIMARY KEY,
              fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
              tipo_evento VARCHAR(50),
              descripcion TEXT,
              nivel_alerta VARCHAR(10)
            );
            ''')
            cur.execute('''
            CREATE TABLE IF NOT EXISTS registros_acceso (
              id INT AUTO_INCREMENT PRIMARY KEY,
              fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
              id_tarjeta VARCHAR(50),
              persona VARCHAR(100),
              estado_bomba VARCHAR(15),
              temperatura FLOAT,
              humedad FLOAT,
              acceso_autorizado BOOLEAN,
              observacion TEXT
            );
            ''')
        conn.commit()
        return jsonify({'status':'ok'}), 201
    finally:
        conn.close()

@app.route('/api/sensores/ambiente', methods=['POST'])
def post_ambiente():
    data = request.get_json(force=True)
    temp = data.get('temperatura')
    hum = data.get('humedad')
    estado = data.get('estado_bomba', 'Apagada')
    alerta = data.get('alerta', '')
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO registros_ambiente (temperatura, humedad, estado_bomba, alerta) VALUES (%s,%s,%s,%s)', (temp, hum, estado, alerta))
        conn.commit()
        return jsonify({'status':'ok'}), 201
    finally:
        conn.close()


def query_table(table, where_clause=None, params=()):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = f"SELECT * FROM {table}"
            if where_clause:
                sql += " WHERE " + where_clause
            sql += " ORDER BY fecha DESC LIMIT 1000"
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        conn.close()


@app.route('/api/ambiente', methods=['GET'])
def get_ambiente():
    # filtros: desde, hasta, limit
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')
    clauses = []
    params = []
    if desde:
        clauses.append('fecha >= %s')
        params.append(desde)
    if hasta:
        clauses.append('fecha <= %s')
        params.append(hasta)
    where = ' AND '.join(clauses) if clauses else None
    rows = query_table('registros_ambiente', where, tuple(params))
    return jsonify(rows)


@app.route('/api/seguridad', methods=['GET'])
def get_seguridad():
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')
    clauses = []
    params = []
    if desde:
        clauses.append('fecha >= %s')
        params.append(desde)
    if hasta:
        clauses.append('fecha <= %s')
        params.append(hasta)
    where = ' AND '.join(clauses) if clauses else None
    rows = query_table('registros_seguridad', where, tuple(params))
    return jsonify(rows)


@app.route('/api/accesos', methods=['GET'])
def get_accesos():
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')
    clauses = []
    params = []
    if desde:
        clauses.append('fecha >= %s')
        params.append(desde)
    if hasta:
        clauses.append('fecha <= %s')
        params.append(hasta)
    where = ' AND '.join(clauses) if clauses else None
    rows = query_table('registros_acceso', where, tuple(params))
    return jsonify(rows)


@app.route('/api/report', methods=['GET'])
def get_report():
    # Params: desde, hasta
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')
    ambiente = query_table('registros_ambiente', 'fecha >= %s AND fecha <= %s' if desde and hasta else None,
                           tuple([desde, hasta]) if desde and hasta else ())
    # generar PDF simple
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    w, h = letter
    p.setFont('Helvetica', 12)
    p.drawString(40, h-40, 'Reporte Invernadero')
    y = h-80
    p.drawString(40, y, 'Registros Ambiente:')
    y -= 20
    for r in ambiente[:40]:
        line = f"{r.get('fecha')} T:{r.get('temperatura')} H:{r.get('humedad')} B:{r.get('estado_bomba')}"
        p.drawString(40, y, line[:120])
        y -= 14
        if y < 60:
            p.showPage()
            p.setFont('Helvetica', 12)
            y = h-40
    p.save()
    buffer.seek(0)
    return send_file_bytes(buffer.getvalue(), filename='reporte_invernadero.pdf')


def send_file_bytes(bts, filename='file.pdf'):
    from flask import Response
    return Response(bts, mimetype='application/pdf', headers={
        'Content-Disposition': f'attachment; filename="{filename}"'
    })

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:p>')
def static_files(p):
    return send_from_directory('static', p)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
