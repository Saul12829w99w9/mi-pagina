import os
import json
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['JSON_FILE'] = 'datos.json'

# Asegurar que existan carpetas necesarias
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def cargar_datos():
    if os.path.exists(app.config['JSON_FILE']):
        with open(app.config['JSON_FILE'], 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def guardar_datos(data):
    with open(app.config['JSON_FILE'], 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def registrar():
    datos = cargar_datos()

    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    constante = request.form.get('constante')
    corriente = request.form.get('corriente')
    procedencia = request.form.get('procedencia')
    año = request.form.get('año')
    fase = request.form.get('fase')
    hilos = request.form.get('hilos')
    descripcion = request.form.get('descripcion')
    imagen = request.files.get('imagen')

    nombre_archivo = ''
    if imagen and imagen.filename:
        nombre_archivo = imagen.filename
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo))

    nuevo = {
        'Marca': marca,
        'Modelo': modelo,
        'Constante': constante,
        'Corriente': corriente,
        'Procedencia': procedencia,
        'Año': año,
        'Fase': fase,
        'Hilos': hilos,
        'Descripcion': descripcion,
        'Imagen': nombre_archivo
    }

    datos.append(nuevo)
    guardar_datos(datos)
    return redirect(url_for('visualizador'))

@app.route('/visualizador')
def visualizador():
    datos = cargar_datos()
    return render_template('visualizador.html', medidores=datos)

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    datos = cargar_datos()
    if 0 <= id < len(datos):
        imagen = datos[id].get('Imagen')
        if imagen:
            ruta = os.path.join(app.config['UPLOAD_FOLDER'], imagen)
            if os.path.exists(ruta):
                os.remove(ruta)
        datos.pop(id)
        guardar_datos(datos)
    return redirect(url_for('visualizador'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    datos = cargar_datos()
    if request.method == 'POST':
        if 0 <= id < len(datos):
            datos[id]['Marca'] = request.form.get('marca')
            datos[id]['Modelo'] = request.form.get('modelo')
            datos[id]['Constante'] = request.form.get('constante')
            datos[id]['Corriente'] = request.form.get('corriente')
            datos[id]['Procedencia'] = request.form.get('procedencia')
            datos[id]['Año'] = request.form.get('año')
            datos[id]['Fase'] = request.form.get('fase')
            datos[id]['Hilos'] = request.form.get('hilos')
            datos[id]['Descripcion'] = request.form.get('descripcion')

            imagen = request.files.get('imagen')
            if imagen and imagen.filename:
                nombre_archivo = imagen.filename
                imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo))
                datos[id]['Imagen'] = nombre_archivo

            guardar_datos(datos)
        return redirect(url_for('visualizador'))

    medidor = datos[id] if 0 <= id < len(datos) else {}
    return render_template('editar.html', medidor=medidor, id=id)

# Archivos estáticos
@app.route('/static/img/<filename>')
def imagen(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
