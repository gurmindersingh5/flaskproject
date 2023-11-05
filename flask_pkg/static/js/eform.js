
let selectedValue;

// entryform: select a customer 
entryForm = document.getElementById('EntryForm');

entryForm.addEventListener('change', function(e) {
  e.preventDefault();
  // Get the selected value from the dropdown_select_Element
  const dropdown = document.getElementById('Customer_name');
  selectedValue = dropdown.options[dropdown.selectedIndex].text;
  // console.log('text', selectedValue)

  // Update innerHTMl
  document.getElementById('cust-address').innerHTML = selectedValue;
  // Set value of HiddenInpId

  const hiddenInp_id = document.getElementById("hiddenInpId");
  hiddenInp_id.value = dropdown.options[dropdown.selectedIndex].value
  // console.log('value',hiddenInp_id.value)
  // console.log(hiddenInp_id.value);
});


//entry form: Parts
  let selectedPart;
  let selectedPrice;

  entryForm2 = document.getElementById('EntryForm2');

  entryForm2.addEventListener('change', function(event) {
  event.preventDefault();

  // Updating hidden input Part
  const Part_dropdown = document.getElementById('part');

  selectedPart = Part_dropdown.options[Part_dropdown.selectedIndex].text;
  const hiddenInp_part = document.getElementById('hiddenInpPart');
  hiddenInp_part.value = selectedPart;

  //fetching price for selected part from server using POST request AJAX
  var price;
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/eform", true);

  xhr.onload=function(){
    price = JSON.parse(this.responseText)['price'];

  // Updating hidden input Price
  const hiddenInp_price = document.getElementById('hiddenInpPrice');
  hiddenInp_price.value = price

  document.getElementById('price-input').value = price;

  };

  xhr.send(selectedPart);

 
  // console.log(hiddenInp_part.value);
});


// setting up styles on div_note
const divNote = document.getElementById('div_note');

if(divNote.textContent.trim() === ""){
    divNote.style.opacity = "0%"
}else{
    divNote.style.opacity = "100%";
    divNote.addEventListener('mouseover', ()=>{divNote.style.opacity="100%";
  setTimeout(function(){
    divNote.style.opacity = "0%";

},3000)
});
}
