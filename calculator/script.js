let query = document.getElementById("query");

let clearButton = document.getElementById("C");
let divideButton = document.getElementById("÷");
let sevenButton = document.getElementById("7");
let eightButton = document.getElementById("8");
let nineButton = document.getElementById("9");
let multiplyButton = document.getElementById("x");
let fourButton = document.getElementById("4");
let fiveButton = document.getElementById("5");
let sixButton = document.getElementById("6");
let subtractButton = document.getElementById("-");
let oneButton = document.getElementById("1");
let twoButton = document.getElementById("2");
let threeButton = document.getElementById("3");
let addButton = document.getElementById("+");
let zeroButton = document.getElementById("0");
let decimalButton = document.getElementById(".");
let returnButton = document.getElementById("<=");
let submitButton = document.getElementById("=");

let queryString = query.textContent;
let operations = ["÷","x","-","+","."];
let dwaboutthislol = ["÷","x","-","+"];

clearButton.onclick = function(){
    query.textContent = 0;
}

divideButton.onclick = function(){
    //operations.includes(query.textContent.at(-1)) ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "÷" : query.textContent += "÷";
    if (isOperands(query.textContent)){
        dwaboutthislol.includes(query.textContent.at(-1)) ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "÷" : {};
    }
    else{
        query.textContent += "÷";
    }
}

multiplyButton.onclick = function(){
    if (isOperands(query.textContent)){
        dwaboutthislol.includes(query.textContent.at(-1)) ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "x" : {};
    }
    else{
        query.textContent += "x";
    }
}

subtractButton.onclick = function(){
    if (isOperands(query.textContent)){
        dwaboutthislol.includes(query.textContent.at(-1)) ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "-" : {};
    }
    else{
        query.textContent += "-";
    }
}

addButton.onclick = function(){
    if (isOperands(query.textContent)){
        dwaboutthislol.includes(query.textContent.at(-1)) ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "+" : {};
    }
    else{
        query.textContent += "+";
    }
}



nineButton.onclick = function(){
    query.textContent.at(0) === "0" && query.textContent.length === 1 ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "9" : query.textContent += "9";
}

eightButton.onclick = function(){
    query.textContent.at(0) === "0" && query.textContent.length === 1 ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "8" : query.textContent += "8";
}

sevenButton.onclick = function(){
    query.textContent.at(0) === "0" && query.textContent.length === 1 ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "7" : query.textContent += "7";
}

sixButton.onclick = function(){
    query.textContent.at(0) === "0" && query.textContent.length === 1 ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "6" : query.textContent += "6";
}

fiveButton.onclick = function(){
    query.textContent.at(0) === "0" && query.textContent.length === 1 ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "5" : query.textContent += "5";
}

fourButton.onclick = function(){
    query.textContent.at(0) === "0" && query.textContent.length === 1 ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "4" : query.textContent += "4";
}

threeButton.onclick = function(){
    query.textContent.at(0) === "0" && query.textContent.length === 1 ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "3" : query.textContent += "3";
}

twoButton.onclick = function(){
    query.textContent.at(0) === "0" && query.textContent.length === 1 ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "2" : query.textContent += "2";
}

oneButton.onclick = function(){
    query.textContent.at(0) === "0" && query.textContent.length === 1 ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "1" : query.textContent += "1";
}

zeroButton.onclick = function(){
    query.textContent.at(0) === "0" && query.textContent.length === 1 ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "0" : query.textContent += "0";
}



decimalButton.onclick = function(){
    //operations.includes(query.textContent.at(-1)) ? query.textContent = query.textContent.substr(0,query.textContent.length-1) + "." : query.textContent += ".";;
    queryString = query.textContent;
    if (isOperands(queryString)){
        for (let i=0; i<queryString.length; i+=1){
            if (dwaboutthislol.includes(queryString[i])){
            theNumber = queryString.substring(i+1);
            break;
            }
        }
    }
    else {
        theNumber = queryString;
    }
    if (theNumber.includes(".")){}
    else{
        query.textContent += ".";
    }
}



returnButton.onclick = function(){
    query.textContent.length > 1 ? query.textContent = query.textContent.substring(0,query.textContent.length-1) : query.textContent = 0;
}



submitButton.onclick = function(){
    queryString = query.textContent;
    for (let i=0; i<queryString.length; i+=1){
        if (dwaboutthislol.includes(queryString[i])){
            let operand = queryString[i];
            let number1 = queryString.substring(0,i);
            let number2 = queryString.substring(i+1);
            if (number2 === "" || isNaN(number2))
            {
                query.textContent = number1;
                return;
            }
            number1 = Number(number1);
            number2 = Number(number2);
            if (operand === "+"){
                query.textContent = number1 + number2;
            }
            else if (operand === "-"){
                query.textContent = number1 - number2;
            }
            else if (operand === "x"){
                query.textContent = number1 * number2;
            }
            else if (operand === "÷"){
                if (number2 === 0){
                    query.textContent = 0;
                }
                else{
                    query.textContent = number1 / number2;
                }
            }
            console.log(operand,number1,number2);
        }
        else{}
    }
}



function isOperands(string){
    for (let i=0;i<string.length;i+=1){
        if (dwaboutthislol.includes(string[i])){return true;}
    }
    return false;
}




