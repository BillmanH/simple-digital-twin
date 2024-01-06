{% load static %}

const canvas = document.getElementById("renderCanvas");
const context = canvas.getContext("2d");

const image = new Image();
image.src = "{% sas_url %}";

image.onload = function() {
    context.drawImage(image, 0, 0, canvas.width, canvas.height);
};

