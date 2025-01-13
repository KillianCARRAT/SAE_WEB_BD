console.log("Script ajout_seance.js");
document.getElementById("hebdo").addEventListener("change", function () {
  console.log("Change detected");
  if (!document.getElementById("hebdo").checked) {
    document.getElementById("semaine_seance").style.display = "grid";
    document
      .getElementById("jour_seance")
      .style.setProperty("display", "none", "important");
  } else {
    document
      .getElementById("semaine_seance")
      .style.setProperty("display", "none", "important");
    document.getElementById("jour_seance").style.display = "grid";
  }
});
document
  .getElementById("semaine_seance")
  .style.setProperty("display", "none", "important");
document.getElementById("hebdo").checked = true;
