const image = document.getElementById("picture");
const nextButton = document.getElementById("next");
const prevButton = document.getElementById("previous");

let currentImage = 1;


nextButton.onclick = function(){
    currentImage++;
    if (currentImage > 3){
        currentImage = 1;
    }
    image.classList.replace("appear","disappear");
    setTimeout(() => {image.setAttribute('src',`images/pic${currentImage}.png`);
    image.classList.replace("disappear","appear");},500);
}
prevButton.onclick = function(){
    currentImage--;
    if (currentImage < 1){
        currentImage = 3;
    }
    image.classList.replace("appear","disappear");
    setTimeout(() => {image.setAttribute('src',`images/pic${currentImage}.png`);
    image.classList.replace("disappear","appear");},500);
}