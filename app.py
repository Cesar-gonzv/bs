from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)
# Crear tabla si no existe
def init_db():
   conn = sqlite3.connect('database.db')
   c = conn.cursor()
   c.execute('''
       CREATE TABLE IF NOT EXISTS ordenes (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           nombre_cliente TEXT,
           correo TEXT,
           telefono TEXT,
           descripcion_servicio TEXT,
           fecha TEXT
       )
   ''')
   conn.commit()
   conn.close()
init_db()
@app.route('/')
def index():
   return render_template('index.html')
@app.route('/guardar', methods=['POST'])
def guardar():
   datos = request.form
   conn = sqlite3.connect('database.db')
   c = conn.cursor()
   c.execute('''
       INSERT INTO ordenes (nombre_cliente, correo, telefono, descripcion_servicio, fecha)
       VALUES (?, ?, ?, ?, ?)
   ''', (datos['nombre'], datos['correo'], datos['telefono'], datos['descripcion'], datos['fecha']))
   conn.commit()
   conn.close()
   return redirect('/')
if __name__ == '__main__':
   app.run(debug=True)