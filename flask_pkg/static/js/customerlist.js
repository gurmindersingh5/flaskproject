



var listofItems = document.getElementsByClassName('alt-row-color');

var listofItems = document.getElementsByClassName('alt-row-color');

for (var i = 0; i < listofItems.length; i++) {
  (function() {
    var originalColor = listofItems[i].style.backgroundColor;

    listofItems[i].addEventListener('mouseover', function () {
      this.style.backgroundColor = "rgb(110, 183, 202)";
      this.style.color = "white";
    });

    listofItems[i].addEventListener('mouseout', function () {
      this.style.backgroundColor = originalColor;
      this.style.color = "";
    });
  })();
}


// for (var i = 0; i < listofItems.length; i++) {

//   var orignalcolor = listofItems[i].style.backgroundColor;

//   listofItems[i].addEventListener('mouseover', function () { this.style.backgroundColor="rgb(110, 183, 202)"});
//   listofItems[i].addEventListener('mouseover', function () { this.style.color="white"});
//   listofItems[i].addEventListener('mouseout', function () { this.style.backgroundColor = orignalcolor});
//   listofItems[i].addEventListener('mouseout', function () { this.style.color = ""});
// };

// Get the "Name" column header
//const nameHeader = document.querySelector('#name-header');

// Add an event listener for when the header is clicked
//nameHeader.addEventListener('click', function() {
  // Toggle the "sorted" class on the header
  //nameHeader.classList.toggle('sorted');
//});


