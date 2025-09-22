const filefield = document.getElementById("filefield");
const preview = document.getElementById("preview");



filefield.addEventListener("change",function() {
    const file = this.files[0];
    if (file){
        const reader = new FileReader();

        reader.onload = function(e) {
      preview.src = e.target.result;   // Set preview image src
      preview.style.display = "block"; // Show the image
    }
    reader.readAsDataURL(file); // Read file as a base64 URL
  } 
  
  
  else {
    preview.style.display = "none"; // Hide if no file selected
  }
});