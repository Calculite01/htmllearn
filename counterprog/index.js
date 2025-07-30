let value = Number(document.getElementById("number").textContent);

document.getElementById("previous").onclick = function(){
    value-=1;
    document.getElementById("number").textContent = value;
}
document.getElementById("reset").onclick = function(){
    value=0;
    document.getElementById("number").textContent = value;
}
document.getElementById("next").onclick = function(){
    value+=1;
    document.getElementById("number").textContent = value;
}
