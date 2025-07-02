# password_evolution.py

import sqlite3
import hashlib
from flask import Flask, request

app = Flask(__name__)
db_name = 'test.db'

@app.route('/')
def index():
    return 'Bienvenido al sistema de evolución de contraseñas - DRY7122'

#########################################
# Registro con contraseña en texto plano
#########################################
@app.route('/signup/v1', methods=['POST'])
def signup_v1():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_PLAIN
                 (USERNAME TEXT PRIMARY KEY NOT NULL,
                  PASSWORD TEXT NOT NULL);''')
    conn.commit()
    try:
        c.execute("INSERT INTO USER_PLAIN (USERNAME, PASSWORD) VALUES (?, ?)", 
                  (request.form['username'], request.form['password']))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Nombre de usuario ya registrado (v1)."
    return "Registro exitoso (v1)"

def verify_plain(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = ?", (username,))
    record = c.fetchone()
    conn.close()
    if not record:
        return False
    return record[0] == password

@app.route('/login/v1', methods=['POST'])
def login_v1():
    if verify_plain(request.form['username'], request.form['password']):
        return 'Inicio de sesión exitoso (v1)'
    else:
        return 'Usuario/Contraseña inválidos (v1)'

#########################################
# Registro con contraseña hasheada SHA256
#########################################
@app.route('/signup/v2', methods=['POST'])
def signup_v2():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH
                 (USERNAME TEXT PRIMARY KEY NOT NULL,
                  HASH TEXT NOT NULL);''')
    conn.commit()
    try:
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH) VALUES (?, ?)", 
                  (request.form['username'], hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Nombre de usuario ya registrado (v2)."
    return "Registro exitoso (v2)"

def verify_hash(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT HASH FROM USER_HASH WHERE USERNAME = ?", (username,))
    record = c.fetchone()
    conn.close()
    if not record:
        return False
    return record[0] == hashlib.sha256(password.encode()).hexdigest()

@app.route('/login/v2', methods=['POST'])
def login_v2():
    if verify_hash(request.form['username'], request.form['password']):
        return 'Inicio de sesión exitoso (v2)'
    else:
        return 'Usuario/Contraseña inválidos (v2)'

# Ejecutar en puerto 5800 con certificado auto firmado
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800, ssl_context='adhoc')
