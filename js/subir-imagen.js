// Configuración de AWS
AWS.config.update({
    accessKeyId: 'AKIA5NXILMPQJDZE4E2E',
    secretAccessKey: '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',
    region: 'us-east-1', // Ejemplo: 'us-east-1'
});

const s3 = new AWS.S3();
const bucketName = 'tpfinal-python';

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
            ACL: 'public-read', // Esto hace que la imagen sea pública
        };

        uploadPromises.push(s3.upload(params).promise());
    }

    // Esperar a que todas las promesas de carga se completen
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
