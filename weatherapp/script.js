const api_key = '88ed465cf7f9014358738bd6a30127c6';
const cityInput = document.getElementById("city");
const resultBox = document.getElementById("result");


async function fetchWeather(){
    const city = cityInput.value;
    let cityLat
    let cityLon

    const response = await fetch(`http://api.openweathermap.org/geo/1.0/direct?q=${city}&appid=${api_key}`);


    const jsonresponse = await response.json();
    try{
        cityLat = jsonresponse[0].lat;
        cityLon = jsonresponse[0].lon;
    }
    catch(error){
        console.log("Invalid City");
        resultBox.textContent = "Invalid City";
        return;
    }

    const response2 = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${cityLat}&lon=${cityLon}&appid=${api_key}`);
    const jsonresponse2 = await response2.json();
    const temp = Math.round(jsonresponse2.main.temp -273.15);
    const desc = jsonresponse2.weather[0].description;
    resultBox.textContent = `Temperature in ${city} is ${temp}°C and has ${desc}`
}

