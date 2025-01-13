function receiveAgendaJsonApi() {
  fetch("/seances/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
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

function displayAgenda(seances) {
  if (!seances) {
    console.error("No seances data available");
    return;
  }

  const container = document.createElement("div");
  // 7 colonnes : 1 pour l’heure, 6 pour les jours
  container.style.display = "grid";
  container.style.gridTemplateColumns = "repeat(7, 1fr)";
  container.style.gridTemplateRows = "50px repeat(48, 20px)";
  container.style.gap = "1px";

  // Entête "Heure" en colonne 1
  const hourHeader = document.createElement("div");
  hourHeader.textContent = "Heure/Jour";
  hourHeader.style.border = "1px solid black";
  hourHeader.style.fontWeight = "bold";
  hourHeader.style.gridRow = "1 / 2";
  hourHeader.style.gridColumn = "1 / 2";
  container.appendChild(hourHeader);

  // En-têtes des 6 jours
  const days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"];
  days.forEach((day, index) => {
    const dayCell = document.createElement("div");
    dayCell.textContent = day;
    dayCell.style.border = "1px solid black";
    dayCell.style.fontWeight = "bold";
    dayCell.style.gridRow = "1 / 2";
    dayCell.style.gridColumn = `${index + 2} / ${index + 3}`;
    container.appendChild(dayCell);
  });

  // Colonne des horaires
  for (let h = 8; h <= 20; h++) {
    const rowBase = 2 + (h - 8) * 2;

    const timeCell = document.createElement("div");
    timeCell.textContent = `${h}:00`;
    timeCell.style.border = "1px solid black";
    timeCell.style.gridColumn = "1 / 2";
    timeCell.style.gridRow = `${rowBase} / ${rowBase + 2}`;
    container.appendChild(timeCell);

    const halfHourCell = document.createElement("div");
    halfHourCell.textContent = `${h}:30`;
    halfHourCell.style.border = "1px solid black";
    halfHourCell.style.gridColumn = "1 / 2";
    halfHourCell.style.gridRow = `${rowBase + 1} / ${rowBase + 2}`;
    container.appendChild(halfHourCell);
  }

  // Cases vides pour 6 jours
  for (let dayIndex = 0; dayIndex < 6; dayIndex++) {
    for (let h = 8; h <= 20; h++) {
      const rowBase = 2 + (h - 8) * 2;

      const cellHour = document.createElement("div");
      cellHour.style.border = "1px solid black";
      cellHour.style.gridColumn = `${dayIndex + 2}`;
      cellHour.style.gridRow = `${rowBase} / ${rowBase + 2}`;
      container.appendChild(cellHour);

      const cellHalfHour = document.createElement("div");
      cellHalfHour.style.border = "1px solid black";
      cellHalfHour.style.gridColumn = `${dayIndex + 2}`;
      cellHalfHour.style.gridRow = `${rowBase + 1} / ${rowBase + 2}`;
      container.appendChild(cellHalfHour);
    }
  }

  // Placement des séances
  seances.forEach((jour, jourIndex) => {
    // Assurer que jourIndex < 6
    if (jourIndex < 6) {
      jour.forEach((seance) => {
        const [startHour, startMinute] = seance.heure_debut_seance
          .split(":")
          .map(Number);
        const [endHour, endMinute] = seance.heure_fin_seance
          .split(":")
          .map(Number);

        const startRow = 2 + (startHour - 8) * 2 + Math.floor(startMinute / 30);
        const totalStart = startHour * 60 + startMinute;
        const totalEnd = endHour * 60 + endMinute;
        const halfHours = Math.floor((totalEnd - totalStart) / 30);

        const seanceCell = document.createElement("div");
        seanceCell.textContent = `${seance.heure_debut_seance} - ${seance.heure_fin_seance}`;
        seanceCell.style.border = "1px solid black";
        seanceCell.style.backgroundColor = "#cfd8dc";
        seanceCell.style.gridRow = `${startRow} / span ${halfHours}`;
        seanceCell.style.gridColumn = `${jourIndex + 2}`;
        container.appendChild(seanceCell);
      });
    }
  });

  document.body.appendChild(container);
}

receiveAgendaJsonApi();
