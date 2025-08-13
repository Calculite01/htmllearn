timeBox = document.getElementById("time");

startButton = document.getElementById("start");
stopButton = document.getElementById("stop");
resetButton = document.getElementById("reset");

let intervalID = null;
let running = false;
let timeElapsed = 0;
let startTime = null;

// function tick(){
//     milliseconds+=1;
//     timeBox.textContent = msToTime(milliseconds);
// }

// startButton.onclick = function startTimer(){
//     if (running === false){
//         thing = setInterval(tick,10);
//         running = true;
//     }
// }

// stopButton.onclick = () => {clearInterval(thing); running = false};

// resetButton.onclick = () => {clearInterval(thing); milliseconds = 0; timeBox.textContent = msToTime(milliseconds); running = false;};

startButton.onclick = function(){
    if(!running){
        running = true;
        startTime = Date.now();
        intervalID = setInterval(() => {update(Date.now() - startTime + timeElapsed)},10);
    }
}

stopButton.onclick = function(){
    if(running){
        clearInterval(intervalID);
        running = false
        timeElapsed = Date.now() - startTime + timeElapsed;
    }
}

resetButton.onclick = function(){
    clearInterval(intervalID);
    running = false;
    timeElapsed = 0;
    update(0);
}

function update(milliseconds){
    let time = msToTime(milliseconds);
    timeBox.textContent = time;
}

function msToTime(milliseconds){
    let hours = 0;
    let minutes = 0;
    let seconds = 0;
    while (milliseconds >= 1000){
        if (milliseconds >= 3600000){
        milliseconds -= 3600000;
        hours += 1;
        }
        else if (milliseconds >= 60000){
            milliseconds -= 60000;
            minutes += 1;
        } 
        else if (milliseconds >= 1000){
            milliseconds -= 1000;
            seconds += 1;
        }
    }
    return `${hours.toString().padStart(2,0)}:${minutes.toString().padStart(2,0)}:${seconds.toString().padStart(2,0)}:${milliseconds.toString().padStart(3,0)}`;
}

