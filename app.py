from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'tu_usuario_mysql'
app.config['MYSQL_PASSWORD'] = 'tu_contraseña_mysql'
app.config['MYSQL_DB'] = 'tu_base_de_datos_mysql'

mysql = MySQL(app)

# Directorio para almacenar temporalmente las imágenes subidas
UPLOAD_FOLDER = 'C:\xampp\htdocs\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta para subir imágenes
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No se proporcionó ningún archivo'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Comprimir la imagen antes de almacenarla
        compressed_filepath = compress_image(filepath)

        # Guardar la información en la base de datos
        save_to_database(filename, compressed_filepath)

        return jsonify({'message': 'Archivo subido exitosamente'}), 200

    return jsonify({'error': 'Error desconocido'}), 500

# Ruta para obtener todas las imágenes desde la base de datos
@app.route('/images', methods=['GET'])
def get_all_images():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, filename, filepath FROM images")
    result = cur.fetchall()
    cur.close()

    images = [{'id': row[0], 'filename': row[1], 'filepath': row[2]} for row in result]

    return jsonify({'images': images}), 200

def compress_image(filepath):
    # Utilizar la biblioteca Pillow para abrir y comprimir la imagen
    with Image.open(filepath) as img:
        img = img.resize((720, 720))
        compressed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'compressed_' + os.path.basename(filepath))
        img.save(compressed_filepath)
        return compressed_filepath

def save_to_database(filename, filepath):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO images (filename, filepath) VALUES (%s, %s)", (filename, filepath))
    mysql.connection.commit()
    cur.close()

if __name__ == '__main__':
    app.run(debug=True)
