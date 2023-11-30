from flask import Flask, render_template, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# Configuración de Amazon S3
S3_BUCKET_NAME = 'tpfinal-python'
AWS_ACCESS_KEY = 'AKIA5NXILMPQJDZE4E2E'
AWS_SECRET_KEY = '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'

# Configuración de Boto3
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

# Ruta para la página principal
@app.route('/')
def index():
    # Obtener la lista de objetos en el bucket de S3
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)
    archivos = [obj['Key'] for obj in response.get('Contents', [])]

    # Construir URLs completas de las imágenes
    urls_imagenes = [s3.generate_presigned_url('get_object', Params={'Bucket': S3_BUCKET_NAME, 'Key': archivo}) for archivo in archivos]

    return render_template('index.html', urls_imagenes=urls_imagenes)

# Ruta para subir una imagen al bucket
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró el archivo'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'Nombre de archivo no válido'}), 400

        # Subir la imagen al bucket de S3
        s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)

        return jsonify({'mensaje': 'Imagen subida exitosamente'}), 200

    except NoCredentialsError:
        return jsonify({'error': 'Credenciales de Amazon S3 no válidas'}), 500

if __name__ == '__main__':
    app.run(debug=True)
