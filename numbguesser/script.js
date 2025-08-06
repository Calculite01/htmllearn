const guessBox = document.getElementById("guess");
const attempts = document.getElementById("attempts");
const result = document.getElementById("result");
const submit = document.getElementById("submit");

let theNumber
//console.log(typeof(submit));



submit.onclick = function(){
    if (result.textContent === "Correct"){
        return
    }
    guess = guessBox.value
    theNumber = Math.floor(Math.random()*10)+1;
    if (isNaN(guess) || guess === "" || Number(guess) < 1 || Number(guess) > 10){
        result.textContent = "Invalid guess";
    }
    else if (Number(attempts.textContent) === 0){
        return
    }
    else if (Number(guess) === theNumber){
        result.textContent = "Correct";
        return
    }
    else{
        result.textContent = "Incorrect";
        attempts.textContent = Number(attempts.textContent)-1;
        if (Number(attempts.textContent) === 0){
            result.textContent = "You lost";
            return
        }
    }
}


