// container -> id : destination, class: "popup"
// trigger -> class: "popup-btn-open", data-popup: "destination"
// close -> class: "popup-btn-close data-popup: "destination"

// Popup
let btn_open = document.querySelectorAll(".popup-btn-open");
let btn_close = document.querySelectorAll(".popup-btn-close");
let popup = document.querySelectorAll(".popup");

function showPopup(object) {
  console.log("object", object);
  let fond = document.createElement("div");
  fond.id = "fond";
  fond.style.position = "fixed";
  fond.style.opacity = "0.5";
  fond.style.visibility = "visible";
  fond.style.transition = "all 0.5s";
  fond.style.zIndex = "999";
  fond.style.top = "0";
  fond.style.left = "0";
  fond.style.width = "100%";
  fond.style.height = "100%";
  fond.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
  document.body.appendChild(fond);

  object.style.display = "block";
  object.style.opacity = "1";
  object.style.visibility = "visible";
  object.style.transition = "all 0.5s";
  object.style.zIndex = "1000";
  object.style.position = "fixed";
  object.style.top = "50%";
  object.style.left = "50%";
  object.style.backgroundColor = "white";
  object.style.borderRadius = "10px";
  object.style.padding = "20px";
  object.style.border = "1px solid #000";
  object.style.transform = "translate(-50%, -50%)";
}

function hidePopup(object) {
  object.style.display = "none";
  object.style.opacity = "0";
  object.style.visibility = "hidden";
  object.style.transition = "all 0.5s";
  object.style.zIndex = "-1";
  document.body.style.backgroundColor = "";
  let fond = document.getElementById("fond");
  if (fond) {
    fond.style.opacity = "0";
    setTimeout(() => {
      document.body.removeChild(fond);
    }, 500);
  }
}

btn_open.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    console.log("btn", btn.dataset.popup);
    let destination = document.getElementById(btn.dataset.popup);
    showPopup(destination);
  });
});

btn_close.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    let destination = e.target.closest(".popup");
    hidePopup(destination);
  });
});

popup.forEach((pop) => {
  hidePopup(pop);
});
