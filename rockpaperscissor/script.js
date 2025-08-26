const pmove = document.getElementById("player");
const cmove = document.getElementById("computer");
const result = document.getElementById("result");
const pscore = document.getElementById("pscore");
const cscore = document.getElementById("cscore");
const playAgain = document.getElementById("replay");

const moveButtons = document.querySelectorAll(".buttons");

let running = false;

moveButtons.forEach(button => {button.onclick = function(){
    if (running){return;}
    running = true;
    let moves = ["paper","scissors","rock"];
    let playermove = button.textContent.toLowerCase();
    let compmove = moves[Math.floor(Math.random() * 3)];
    pmove.firstElementChild.textContent = playermove;
    cmove.firstElementChild.textContent = compmove;
    pmove.style.visibility = "visible";
    playermove = moves.indexOf(playermove);
    compmove = moves.indexOf(compmove);
    console.log(playermove,compmove);
    if (playermove === compmove){result.textContent="Draw";}
    else if (Math.abs(playermove-compmove) === 2){
        console.log("this is rock paper");
        playermove === 0 ? setWinner("player") : setWinner("computer");
    }
    else{
        console.log("this is normal");
        playermove > compmove ? setWinner("player") : setWinner("computer");
    }
    setTimeout(() => cmove.style.visibility = "visible",700);
    setTimeout(() => result.style.visibility = "visible",1400);
    setTimeout(() => playAgain.style.visibility = "visible",2100);
}})

playAgain.onclick = function(){
    running = false;
    pmove.style.visibility = "hidden";
    cmove.style.visibility = "hidden";
    result.style.visibility = "hidden";
    playAgain.style.visibility = "hidden";
}

function setWinner(winner){
    if (winner === "player"){
        let ting = Number(pscore.firstElementChild.textContent);
        ting+=1;
        setTimeout(() => pscore.firstElementChild.textContent = ting,2100);
        result.textContent = "Player Wins";
    }
    else if (winner === "computer"){
        let ting = Number(cscore.firstElementChild.textContent);
        ting+=1;
        setTimeout(() => cscore.firstElementChild.textContent = ting,2100);
        result.textContent = "Computer Wins";
    }
}

