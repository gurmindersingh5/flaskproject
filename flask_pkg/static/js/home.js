
// Purchases bar graph setup -------------->
const ctx = document.getElementById("purchases").getContext("2d");

var names =  (document.getElementById('data').innerText);
var price =  (document.getElementById('price').innerText);
names = names.split(",");

let prices = price.split(",");

  console.log(names);
  console.log(prices);

        const customerData = {
            labels: [names[0], names[1], names[2], names[3]],
            datasets: [
                {
                    label: "Purchases",
                    data: [prices[0], prices[1], prices[2], prices[3]],
                    backgroundColor: ["blue", "green", "red", "purple"],
                },
            ],
        };

        const customerChart = new Chart(ctx, {
            type: "bar",
            data: customerData,
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                    },
                },
            },
        });






// Monthly sales line graph setup ----------->
      // Get the canvas element
const lineChartCanvas = document.getElementById('monthly-sales');

// let months = document.getElementById('months').textContent;
//let monthly_sale = document.getElementById('monthly_sale').textContent;

// Define the URL for the GET request
const url = '/';

// Define the data you want to send in the request body
const postData = {
  'key': 'montlySalesGraph'
};

$.ajax({
  url: url,
  type: 'POST',
  data: JSON.stringify(postData),
  contentType: 'application/json',
  success: function (data) {
    // Handle the success response here
    var monthly_sale = data['monthly_sale']
    monthly_sale = monthly_sale.reverse()
    var months = data['months']
    const monthlyLabels = {
      1: 'Jan',
      2: 'Feb',
      3: 'Mar',
      4: 'Apr',
      5: 'May',
      6: 'Jun',
      7: 'Jul',
      8: 'Aug',
      9: 'Sep',
      10: 'Oct',
      11: 'Nov',
      12: 'Dec'
    };
    let months_str = []
    for(i=months.length-1;i>=0;i--){
      months_str.push(monthlyLabels[months[i]]);
    }

    // Create a line chart using Chart.js
    const lineChart = new Chart(lineChartCanvas, {
      type: 'line',
      data: {
        labels: months_str,
        datasets: [
          {
            label: 'Monthly Sales',
            data: monthly_sale,
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
    

  },
  error: function (error) {
    // Handle any errors here
    console.log(error);
  }
});





// Get the location from browser's navigator for weather update
var lat, lon;
    if ("geolocation" in navigator) {
        // Geolocation is available
        navigator.geolocation.getCurrentPosition(
        function(position) {
            // Handle successful location retrieval
            lat = position.coords.latitude;
            lon = position.coords.longitude;
            console.log("Latitude:", lat);
            console.log("Longitude:", lon);
        },
        function(error) {
            // Handle location retrieval error
            console.error("Error getting location:", error.message);
        }
        );
    } 
    else {
        // Geolocation is not available
        lat = 30.82;
        lon = 75.17;

    }
      
  // After getting location fetch the weather data from OPENWEATHERMAP website
    setTimeout(function() {
    const Key = '58256befe2c4ca018310daa1c5a9b771';
    //const apiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${Key}&units=metric`;
    fetch(apiUrl)
  .then(response => response.json())
  .then(data => {
    console.log(data);

    // Extract and display weather information
    const temperature = data.main.temp;
    const weatherElement = document.getElementsByClassName('weather-container')[0];

    const weatherDescription = data.weather[0].description;
    const weatherInfo = `Temperature: ${temperature}°C, Description: ${weatherDescription}`;    
    weatherElement.innerHTML = weatherInfo;
    
    if(temperature>20){
        weatherElement.style.transition = '10s';
        weatherElement.style.backgroundColor = "yellow";
      }
      else{
        weatherElement.style.transition = '10s';
        weatherElement.style.backgroundColor = "#2f62c2"
        setTimeout(function(){
            weatherElement.style.color = "white"
        },10000)
      };
  })
  .catch(error => {
    console.error('Error fetching weather data:', error);
  });
  
}, 8000);




// Digital Clock setup
function updateClock() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, "0");
    const minutes = now.getMinutes().toString().padStart(2, "0");
    const seconds = now.getSeconds().toString().padStart(2, "0");
    const timeString = `${hours}:${minutes}:${seconds}`;

    clockElement[0].querySelector('.clock').innerHTML = timeString;
    
  }
  
  const clockElement = document.getElementsByClassName("clock-container");

  setInterval(updateClock, 1000);
  updateClock();

  
  clockElement[0].querySelector('.clock').addEventListener('mouseover', function(){
    clockElement[0].querySelector('.date').style.visibility = "visible";
    clockElement[0].querySelector('.date').style.height = "auto";
    clockElement[0].style.height = "auto";
    clockElement[0].style.backgroundColor = "pink";
    
    const now = new Date()
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    document.getElementById('date').innerHTML = days[now.getDay()];
    document.getElementById('date').innerHTML += "<br>";
    document.getElementById('date').innerHTML +=  now.getDate() + ' ' + months[now.getMonth()] + ', ' + now.getFullYear();

  });
  clockElement[0].querySelector('.clock').addEventListener('mouseout', function(){
    clockElement[0].querySelector('.date').style.visibility = "hidden";
    clockElement[0].querySelector('.date').style.height = '0';
    clockElement[0].style.height = "70px";
    clockElement[0].style.backgroundColor = "transparent";


  });
  

// Calculator working logic setup
    function appendToDisplay(value) {
      document.getElementById('display').value += value;
  }
  function clearDisplay() {
      document.getElementById('display').value = '';
  }
  function calculateResult() {
      try {
          const result = eval(document.getElementById('display').value);
          document.getElementById('display').value = result;
      } catch (error) {
          document.getElementById('display').value = 'Error';
      }
  };
  


// Top Icon container div, Icons setup and working
  var div1 = document.getElementById('div1');
  var calc = document.getElementById('calc');
  var graph = document.getElementById('graph');
  var calcElem = document.getElementById('calcElem');
  var graphElem = document.getElementById('graphElem');
  var bargraphElem = document.getElementById('bargraphElem');

  //calculator on click show/hide + styling
calc.addEventListener('click', function(){
  if (calcElem.style.backgroundColor === "rgb(56, 87, 243)"){
      calcElem.style.backgroundColor = "transparent";
  }else{
      calcElem.style.backgroundColor = "rgb(56, 87, 243)";
  };
  if (div3.style.display === "none" ){
      div3.style.display = "";
  }else{div3.style.display = "none"}
});  

  //graph on click show/hide + styling
graph.addEventListener('click', function(){
  if (graphElem.style.backgroundColor === "rgb(56, 87, 243)"){
      graphElem.style.backgroundColor = "transparent";
  }else{
      graphElem.style.backgroundColor = "rgb(56, 87, 243)";
  };
  if (div2.style.display === "none" ){
      div2.style.display = "";
  }else{div2.style.display = "none"}
});  

  //bar graph on click show/hide + styling
bargraph.addEventListener('click', function(){
  if (bargraphElem.style.backgroundColor === "rgb(56, 87, 243)"){
      bargraphElem.style.backgroundColor = "transparent";
  }else{
      bargraphElem.style.backgroundColor = "rgb(56, 87, 243)";
  };
  if (div1.style.display === "none" ){
      div1.style.display = "";
  }else{div1.style.display = "none"}
});  

