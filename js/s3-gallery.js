// Configuración de AWS
AWS.config.update({
    accessKeyId: 'AKIA5NXILMPQJDZE4E2E',
    secretAccessKey: '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',
    region: 'us-east-1', // Ejemplo: 'us-east-1'
});
  
  const s3 = new AWS.S3();
  const bucketName = 'tpfinal-python';
  
  async function loadImagesFromS3() {
    const galleryDiv = document.getElementById('s3-img-gallery');
  
    try {
      const data = await s3.listObjectsV2({ Bucket: bucketName }).promise();
  
      // Limpiar la galería antes de agregar nuevas imágenes
      galleryDiv.innerHTML = '';
  
      // Recorrer objetos en el bucket y agregar imágenes a la galería
      data.Contents.forEach((object) => {
        const imageUrl = s3.getSignedUrl('getObject', { Bucket: bucketName, Key: object.Key });
  
        const imgElement = document.createElement('img');
        imgElement.src = imageUrl;
        imgElement.alt = '';
        imgElement.onclick = () => openFulImg(imageUrl); // Agregar función para mostrar imagen completa
        galleryDiv.appendChild(imgElement);
      });
    } catch (error) {
      console.error('Error al cargar imágenes desde S3:', error);
    }
  }
  
  // Llamar a la función para cargar imágenes al cargar la página
  window.onload = loadImagesFromS3;
  