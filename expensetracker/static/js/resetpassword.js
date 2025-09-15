const passwordField = document.getElementById("pw");
const confirmPasswordField = document.getElementById("cpw");
const feedback = document.getElementById("feedback");
const extrafeedback = document.getElementById("extrafeedback");


document.addEventListener("keydown",event => {
    setTimeout(passwordCheck,100);
})

function passwordCheck(){
    const password = passwordField.value;
    let strength = 0;
    if (password === ""){
        feedback.textContent = "";
        extrafeedback.textContent = "";
        return;
    }
    if (password.length < 8){
        feedback.textContent = "Password has to be atleast 8 characters";
        return;
    }
    const regex = [/\d/,/[A-Za-z]/,/[^A-Za-z0-9]/];
    for (const re of regex){
        if (re.test(password)){strength++;}
    }
    if (strength < 3){
        feedback.textContent = "Strength: Weak";
        extrafeedback.textContent = "Password must contain atleast 1 letter 1 number and one special character (@$!%*?&)";
    }
    else{feedback.textContent = "Strength: Strong"; extrafeedback.textContent = "";}
}