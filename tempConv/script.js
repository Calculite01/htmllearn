const inputTempBox = document.getElementById("inputbox")
const mode1 = document.getElementById("input1")
const mode2 = document.getElementById("input2")
const calculate = document.getElementById("calculate")
const temp = document.getElementById("temp")
const error = document.getElementById("error")

calculate.onclick = function(){
    if (!(mode1.checked || mode2.checked)){
        error.textContent = "Select a conversion type!"
        return
    }
    if (isNaN(inputTempBox.value) || inputTempBox.value === ""){
        error.textContent = "Invalid temperature!"
        return
    }
    if (mode1.checked){
        temp.textContent = `${((Number(inputTempBox.value)*9/5)+32).toFixed(1)}°F`
    }
    else if (mode2.checked){
        temp.textContent = `${((Number(inputTempBox.value)-32)*5/9).toFixed(1)}°C`
    }
    error.textContent = ""
}