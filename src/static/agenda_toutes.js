// Variables globales pour gérer l’année/semaine
let currentYear = new Date().getFullYear();
let currentWeek = (function getISOWeek(date) {
  date = new Date(date.getTime());
  date.setHours(0, 0, 0, 0);
  date.setDate(date.getDate() + 4 - (date.getDay() || 7));
  let yearStart = new Date(date.getFullYear(), 0, 1);
  return Math.ceil(((date - yearStart) / 86400000 + 1) / 7);
})(new Date());

// Charge les données pour une année et une semaine données
function updateAgenda(year, week) {
  fetch(`/toutes_les_seances/${year}/${week}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      displayAgenda(data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Fonction déclenchée au chargement initial
function receiveAgendaJsonApi() {
  updateAgenda(currentYear, currentWeek);
}

// Navigation entre semaines
function previousWeek() {
  if (currentWeek === 1) {
    currentWeek = 52;
    currentYear--;
  } else {
    currentWeek--;
  }
  updateAgenda(currentYear, currentWeek);
}

function nextWeek() {
  if (currentWeek === 52) {
    currentWeek = 1;
    currentYear++;
  } else {
    currentWeek++;
  }
  updateAgenda(currentYear, currentWeek);
}

// Aller à une semaine précise
function goToWeek() {
  const yearVal = document.getElementById("yearInput").value;
  const weekVal = document.getElementById("weekInput").value;
  currentYear = parseInt(yearVal, 10);
  currentWeek = parseInt(weekVal, 10);
  updateAgenda(currentYear, currentWeek);
}

// Affichage de l'agenda
function displayAgenda(seances) {
  if (!seances) {
    console.error("No seances data available");
    return;
  }

  // Nettoyage précédant pour recharger l'agenda
  const oldContainer = document.getElementById("agendaContainer");
  if (oldContainer) {
    oldContainer.remove();
  }

  // Création du conteneur d'affichage
  const container = document.createElement("div");
  container.id = "agendaContainer";
  container.style.display = "grid";
  container.style.gridTemplateColumns = "repeat(7, 1fr)";
  container.style.gridTemplateRows = "auto repeat(48, 1fr)";
  container.style.gap = "5px"; // Augmenter l'espacement
  container.style.padding = "10px"; // Ajouter du padding

  // Entête « Heure/Jour »
  const hourHeader = document.createElement("div");
  hourHeader.textContent = "Heure/Jour";
  hourHeader.classList.add("bg-secondary", "text-white", "p-2", "rounded");
  hourHeader.style.gridRow = "1 / 2";
  hourHeader.style.gridColumn = "1 / 2";
  container.appendChild(hourHeader);

  // En-têtes des 6 jours (Lundi à Samedi)
  const days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"];
  days.forEach((day, index) => {
    firstDayOfYear = new Date(currentYear, 0, 1);
    daysOffset =
      (currentWeek - 1) * 7 +
      index +
      (firstDayOfYear.getDay() === 0 ? -6 : 1 - firstDayOfYear.getDay());
    date_info = new Date(currentYear, 0, 1 + daysOffset);
    const dayCell = document.createElement("div");
    dayCell.textContent = day + " " + date_info.toLocaleDateString("fr-FR");
    dayCell.classList.add("bg-light", "p-2", "rounded");
    dayCell.style.gridRow = "1 / 2";
    dayCell.style.gridColumn = `${index + 2} / ${index + 3}`;
    container.appendChild(dayCell);
  });

  // Colonne horaires (Parties entières + demi-heures)
  for (let h = 8; h <= 20; h++) {
    const rowBase = 2 + (h - 8) * 2;

    const timeCell = document.createElement("div");
    timeCell.textContent = `${h}:00`;
    timeCell.classList.add("bg-light", "p-1", "rounded");
    timeCell.style.gridColumn = "1 / 2";
    timeCell.style.gridRow = `${rowBase} / ${rowBase + 2}`;
    container.appendChild(timeCell);

    const halfHourCell = document.createElement("div");
    halfHourCell.textContent = `${h}:30`;
    halfHourCell.classList.add("bg-light", "p-1", "rounded");
    halfHourCell.style.gridColumn = "1 / 2";
    halfHourCell.style.gridRow = `${rowBase + 1} / ${rowBase + 2}`;
    container.appendChild(halfHourCell);
  }

  // Cases vides pour chaque demi-heure des 6 jours
  for (let dayIndex = 0; dayIndex < 6; dayIndex++) {
    for (let h = 8; h <= 20; h++) {
      const rowBase = 2 + (h - 8) * 2;

      const cellHour = document.createElement("div");
      cellHour.classList.add("bg-light", "p-1", "rounded");
      cellHour.style.gridColumn = `${dayIndex + 2}`;
      cellHour.style.gridRow = `${rowBase} / ${rowBase + 2}`;
      container.appendChild(cellHour);

      const cellHalfHour = document.createElement("div");
      cellHalfHour.classList.add("bg-light", "p-1", "rounded");
      cellHalfHour.style.gridColumn = `${dayIndex + 2}`;
      cellHalfHour.style.gridRow = `${rowBase + 1} / ${rowBase + 2}`;
      container.appendChild(cellHalfHour);
    }
  }

  // Placement des séances
  seances.forEach((jour, jourIndex) => {
    if (jourIndex < 6) {
      jour.forEach((seance) => {
        if (seance.active == true) {
          const [startHour, startMinute] = seance.heure_debut_seance
            .split(":")
            .map(Number);
          const [endHour, endMinute] = seance.heure_fin_seance
            .split(":")
            .map(Number);

          const startRow =
            2 + (startHour - 8) * 2 + Math.floor(startMinute / 30);
          const totalStart = startHour * 60 + startMinute;
          const totalEnd = endHour * 60 + endMinute;
          const halfHours = Math.floor((totalEnd - totalStart) / 30);

          const seanceCell = document.createElement("div");
          seanceCell.textContent = `${seance.heure_debut_seance} - ${seance.heure_fin_seance}`;
          seanceCell.classList.add("bg-info", "text-white", "p-1", "rounded");
          seanceCell.style.gridRow = `${startRow} / span ${halfHours}`;
          seanceCell.style.gridColumn = `${jourIndex + 2}`;
          container.appendChild(seanceCell);
          seanceCell.addEventListener("click", () => {
            console.log(seance);
            window.location.href = `/home/seance/${seance.id_seance}`;
          });
        }
      });
    }
  });

  document.getElementById("agenda_toutes").appendChild(container);
}

// Ajout d'une zone pour les boutons et champs de navigation
const formContainer = document.createElement("div");
formContainer.classList.add("mb-3"); // Bootstrap margin-bottom

const prevButton = document.createElement("button");
prevButton.innerText = "Semaine précédente";
prevButton.classList.add("btn", "btn-primary", "me-2"); // Bootstrap classes
prevButton.addEventListener("click", previousWeek);
formContainer.appendChild(prevButton);

const nextButton = document.createElement("button");
nextButton.innerText = "Semaine suivante";
nextButton.classList.add("btn", "btn-primary", "me-2"); // Bootstrap classes
nextButton.addEventListener("click", nextWeek);
formContainer.appendChild(nextButton);

const dateLabel = document.createElement("label");
dateLabel.innerText = "Date : ";
dateLabel.classList.add("form-label", "me-2"); // Bootstrap classes

const dateInput = document.createElement("input");
dateInput.type = "date";
dateInput.id = "dateInput";
dateInput.valueAsDate = new Date();
dateInput.classList.add("form-control", "d-inline-block", "w-auto"); // Bootstrap classes
dateLabel.appendChild(dateInput);
formContainer.appendChild(dateLabel);

function update() {
  const selectedDate = new Date(dateInput.value);
  const year = selectedDate.getFullYear();
  const week = (function getISOWeek(date) {
    date = new Date(date.getTime());
    date.setHours(0, 0, 0, 0);
    date.setDate(date.getDate() + 4 - (date.getDay() || 7));
    let yearStart = new Date(date.getFullYear(), 0, 1);
    return Math.ceil(((date - yearStart) / 86400000 + 1) / 7);
  })(selectedDate);
  currentYear = year;
  currentWeek = week;
  updateAgenda(currentYear, currentWeek);
}
dateInput.addEventListener("change", () => {
  update();
});

document.getElementById("agenda_toutes").appendChild(formContainer);

// Lancement initial
receiveAgendaJsonApi();
