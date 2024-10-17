fetch("runtime_log.csv")
  .then((response) => response.text())
  .then((data) => {
    const rows = data.trim().split("\n");
    const headers = rows[0].split(",");
    const table = document.getElementById("data-table");
    const thead = table.querySelector("thead tr");
    const tbody = table.querySelector("tbody");

    headers.forEach((header) => {
      const th = document.createElement("th");
      th.textContent = header;
      thead.appendChild(th);
    });

    const logData = rows.slice(1).map((row) => row.split(","));
    logData.sort((a, b) => new Date(b[0]) - new Date(a[0]));

    const latestTwoRecords = logData.slice(0, 2);

    latestTwoRecords.forEach((row) => {
      const highlightedDiv = document.createElement("div");
      const dateDiv = document.createElement("div");
      dateDiv.classList.add("date");
      dateDiv.textContent = row[0];

      const shiftDiv = document.createElement("div");
      shiftDiv.classList.add("shift");
      shiftDiv.textContent = row[1] + " Shift";

      const runtimeDiv = document.createElement("div");
      runtimeDiv.classList.add("runtime");
      runtimeDiv.textContent = row[2];

      highlightedDiv.appendChild(dateDiv);
      highlightedDiv.appendChild(shiftDiv);
      highlightedDiv.appendChild(runtimeDiv);
      document
        .getElementById("highlighted-results")
        .appendChild(highlightedDiv);
    });

    logData.forEach((row) => {
      const tr = document.createElement("tr");
      row.forEach((column) => {
        const td = document.createElement("td");
        td.textContent = column;
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
  });
