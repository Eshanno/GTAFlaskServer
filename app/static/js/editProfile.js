
function myFunction() {
  var x = document.getElementById("editProfilePic");
  if (x.style.display ==="none" ){
    x.style.display ="inline";
  } else {
    x.style.display = "none";
  }
}


function onHoverReduceTransparency(thing) {

  thing.style.opacity= .9;
  
}

function afterHoverReturnTransparency(thing) {

  thing.style.opacity= .5;
}
