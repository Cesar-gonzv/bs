from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import os
from reportlab.pdfgen import canvas

app = Flask(__name__)
os.makedirs('comprobantes', exist_ok=True)

# Resto del código anterior...

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM ordenes WHERE nombre_cliente = ?', (nombre,))
        datos = c.fetchall()
        conn.close()
        return render_template('buscar.html', datos=datos, nombre=nombre)
    return render_template('buscar.html', datos=None)

@app.route('/comprobante/<int:orden_id>')
def comprobante(orden_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM ordenes WHERE id = ?', (orden_id,))
    orden = c.fetchone()
    conn.close()

    if not orden:
        return "Orden no encontrada", 404

    file_path = f"comprobantes/comprobante_{orden_id}.pdf"
    generar_pdf(file_path, orden)
    return send_file(file_path, as_attachment=True)

def generar_pdf(path, orden):
    c = canvas.Canvas(path)
    c.drawString(100, 800, f"Comprobante de Orden de Servicio N° {orden[0]}")
    c.drawString(100, 770, f"Cliente: {orden[1]}")
    c.drawString(100, 750, f"Correo: {orden[2]}")
    c.drawString(100, 730, f"Teléfono: {orden[3]}")
    c.drawString(100, 710, f"Fecha: {orden[5]}")
    c.drawString(100, 690, "Descripción del servicio:")
    c.drawString(120, 670, orden[4][:90])  # Acortar texto largo
    c.save()