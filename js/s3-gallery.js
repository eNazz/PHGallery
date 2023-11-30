// Configuración de AWS
AWS.config.update({
    accessKeyId: 'AKIA5NXILMPQJDZE4E2E',
    secretAccessKey: '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',
    region: 'us-east-1', // Ejemplo: 'us-east-1'
});

// Crear una nueva instancia de AWS.S3
const s3 = new AWS.S3();
const bucketName = 'NOMBRE_DE_TU_BUCKET';

// Función para subir imágenes
function uploadImages() {
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;

    if (files.length === 0) {
        alert('Selecciona al menos una imagen.');
        return;
    }

    const uploadPromises = [];

    for (const file of files) {
        const fileName = file.name;
        const fileKey = 'uploads/' + fileName;

        const params = {
            Bucket: bucketName,
            Key: fileKey,
            Body: file,
            ACL: 'public-read',
        };

        uploadPromises.push(s3.upload(params).promise());
    }

    Promise.all(uploadPromises)
        .then(() => {
            alert('Imágenes subidas con éxito.');
            // Recargar las imágenes desde S3
            loadImagesFromS3();
        })
        .catch((error) => {
            console.error('Error al subir imágenes:', error);
            alert('Error al subir imágenes.');
        });
}

// Ejecutar la función de carga de imágenes desde S3 al cargar la página
window.onload = loadImagesFromS3;
