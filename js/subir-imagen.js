// ... (Tu código existente)

function openFulImg(reference) {
    const fulImgBox = document.getElementById("fulImgBox");
    const fulImg = document.getElementById("fulImg");

    fulImgBox.style.display = "flex";
    fulImg.src = reference;
}

function closeImg() {
    const fulImgBox = document.getElementById("fulImgBox");
    fulImgBox.style.display = "none";
}

// ... (Tu código existente)
