
  const elem = document.getElementById("div_note");
  elem.addEventListener('mouseover', function(){
    elem.style.fontSize = "larger"
    elem.style.border = "solid"
    elem.style.borderColor = "#01b328"

  });

  elem.addEventListener('mouseout', function(){
    elem.style.fontSize = "large"
    elem.style.border = "collapse"
    elem.style.borderColor = "transparent"

  });
