let searchedSen = 0; // Global variable to store the count of filtered sensors

async function fetchSensorData() {
  try {
    const response = await fetch("http://127.0.0.1:5000/senzory");
    if (!response.ok) {
      throw new Error("Failed to fetch sensor data");
    }
    const sensorData = await response.json();
    return sensorData;
  } catch (error) {
    console.error("Error fetching sensor data:", error);
    return []; // Return empty array if there's an error
  }
}

async function fetchHistoricalDelay(sensor_id) {
  const response = await fetch(
    `http://localhost:5000/historical/${sensor_id}/delay`
  );
  return await response.json();
}

// /historical/{sensor_id}/frequency

async function fetchFrequency() {
  const response = await fetch(`http://localhost:5000/frequency`);
  return await response.json();
}

async function fetchSensorCount() {
  try {
    const response = await fetch("http://127.0.0.1:5000/pocetsenzoru");
    if (!response.ok) {
      throw new Error("Failed to fetch sensor count");
    }
    const countData = await response.json();
    return countData.count;
  } catch (error) {
    console.error("Error fetching sensor count:", error);
    return 0; // Return 0 if there's an error
  }
}

async function fetchRecordsInLastMinute() {
  try {
    const response = await fetch("http://127.0.0.1:5000/pocetzaminutu");
    if (!response.ok) {
      throw new Error("Failed to fetch records in the last minute");
    }
    const countData = await response.json();
    return countData.count;
  } catch (error) {
    console.error("Error fetching records in the last minute:", error);
    return 0; // Return 0 if there's an error
  }
}
async function fetchAndCreateGraph() {
  try {
    const response = await fetch("http://127.0.0.1:5000/grafzaznamu/raw");
    const data = await response.json();

    // Přidání logování
    console.log("Načtená data:", data);

    // Připravit data pro Plotly
    const dates = data.map((record) => record.cas);
    const counts = dates.reduce((acc, date) => {
      acc[date] = (acc[date] || 0) + 1;
      return acc;
    }, {});

    console.log("Data pro graf - dates:", dates);
    console.log("Data pro graf - counts:", counts);

    const trace = {
      x: dates,
      y: counts,
      type: "scatter",
    };

    const layout = {
      title: "Počet záznamů za den",
      xaxis: { title: "Datum" },
      yaxis: { title: "Počet záznamů" },
    };

    Plotly.newPlot("graph1", [trace], layout);
  } catch (error) {
    console.error("Error:", error);
  }
}

function saveScrollPosition() {
  localStorage.setItem("scrollPosition", window.scrollY);
}

function restoreScrollPosition() {
  const scrollPosition = localStorage.getItem("scrollPosition");
  if (scrollPosition) {
    window.scrollTo(0, parseFloat(scrollPosition));
  }
}

async function generateSensorCards() {
  const sensors = await fetchSensorData();
  const sensorCount = await fetchSensorCount();
  const recordsInLastMinute = await fetchRecordsInLastMinute();

  const sensorsContainer = document
    .getElementById("sensors")
    .querySelector(".row");
  const summaryContainer = document.getElementById("summary");

  summaryContainer.innerHTML = `
        <h5>Celkový počet senzorů: ${sensorCount}</h5>
        <h5>Počet vyhledaných senzorů: ${searchedSen}</h5>
        <h5>Počet záznamů za poslední minutu: ${recordsInLastMinute}</h5>
    `;

  const query = document
    .getElementById("sensor-search")
    .value.trim()
    .toLowerCase();

  sensorsContainer.innerHTML = ""; // Clear existing cards
  let delay = 0;

  sensors.forEach((sensor) => {
    if (!query || sensor.typ.toLowerCase().includes(query)) {
      const card = document.createElement("div");
      card.className = "card p-3 rounded-3 shadow";
      card.style.borderColor = sensor.stav;
      card.innerHTML = `
                <div class="row sensor-details">
                    <div class="col-md-10 sensor-info">
                        <h5 class="card-title">${sensor.nazev}</h5>
                        <p class="card-text">
                            ID: ${sensor.id} | Počet Zápisů: ${
                              sensor.count_records
                            } | Typ: ${sensor.typ} | Místo: ${
                              sensor.misto
                            } | Frekvence: ${sensor.frekvence} | Počasí: ${
                              sensor.weather || "N/A"
                            }
                        </p>
                    </div>
                    <div class="col-md-2 d-flex align-items-center">
                        <div class="status-circle" style="background-color: ${
                          sensor.stav
                        };"></div>
                    </div>
                </div>
            `;
      card.addEventListener("click", function () {
        showModal(sensor);
      });
      sensorsContainer.appendChild(card);
      searchedSen++;
    }
  });

  // Ensure the summary is updated correctly with the count of displayed sensors
  summaryContainer.querySelector("h5:nth-child(2)").textContent =
    `Počet vyhledaných senzorů: ${searchedSen}`;

  // Restore the scroll position after updating the sensor cards
  restoreScrollPosition();
}

// Save the scroll position before refreshing sensor cards
window.addEventListener("beforeunload", saveScrollPosition);

// Refresh sensor cards every 1 minute without scrolling to the top or playing the animation
setInterval(() => {
  saveScrollPosition();
  generateSensorCards();
}, 60000);

window.addEventListener("DOMContentLoaded", async (event) => {
  const currentTheme = "dark";
  updatePlotlyTheme(currentTheme);
  updateNavbarLogo(currentTheme);
  await generateSensorCards(); // Generate initial sensor cards
  await fetchAndCreateGraph();
  restoreScrollPosition(); // Restore scroll position after generating initial cards
});

function updatePlotlyTheme(theme) {
  const layout =
    theme === "light"
      ? {
          paper_bgcolor: "#ffffff",
          plot_bgcolor: "#ffffff",
          font: { color: "#000000" },
        }
      : {
          paper_bgcolor: "#121212",
          plot_bgcolor: "#121212",
          font: { color: "#ffffff" },
        };

  const sensorGraphElement = document.getElementById("sensorGraph");
  if (sensorGraphElement.data) {
    Plotly.relayout(sensorGraphElement, layout);
  }
}

function updateNavbarLogo(theme) {
  const logo = document.getElementById("navbar-logo");
  logo.src =
    theme === "light" ? "images/Scenix.png" : "images/ScenixDarkTheme.png";
}

const themeToggleBtn = document.getElementById("theme-toggle");
const themeStyle = document.getElementById("theme-style");

themeToggleBtn.addEventListener("click", () => {
  const currentTheme = themeStyle.getAttribute("href").includes("dark")
    ? "dark"
    : "light";
  const newTheme = currentTheme === "dark" ? "light" : "dark";

  themeStyle.setAttribute("href", `css/${newTheme}-theme.css`);
  updatePlotlyTheme(newTheme);
  updateNavbarLogo(newTheme);
});

const modal = document.getElementById("modal");
const span = document.getElementsByClassName("close")[0];
async function showModal(sensor) {
  modal.style.display = "flex";
  console.log(sensor.id);

  try {
    const data = await fetchHistoricalDelay(sensor.id);
    console.log(data);

    const sensorGraphData = [
      {
        x: data.data.map((record) => record.timestamp),
        y: data.data.map((record) => record.delay),
        type: "scatter",
        mode: "lines+markers",
        name: `Historický delay pro sensor ${sensor.nazev}`,
      },
    ];

    Plotly.newPlot("sensorGraph", sensorGraphData, {
      title: `Historický delay pro sensor ${sensor.nazev}`,
      xaxis: { title: "Čas" },
      yaxis: { title: "Zpoždění (sekundy)" },
    });
  } catch (error) {
    console.error("Error fetching historical delay:", error);
  }
}

span.onclick = function () {
  modal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
};

const homepageLink = document.getElementById("nav-homepage");
const sensorsLink = document.getElementById("nav-sensors");

homepageLink.addEventListener("click", function () {
  document.getElementById("homepage").classList.remove("hidden");
  document.getElementById("sensors").classList.add("hidden");
  this.classList.add("active");
  sensorsLink.classList.remove("active");
});

sensorsLink.addEventListener("click", function () {
  document.getElementById("homepage").classList.add("hidden");
  document.getElementById("sensors").classList.remove("hidden");
  this.classList.add("active");
  homepageLink.classList.remove("active");
});

const sensorSearchInput = document.getElementById("sensor-search");
sensorSearchInput.addEventListener("input", function () {
  const query = this.value.trim().toLowerCase();
  searchedSen = 0; // Reset the count before filtering
  filterSensorCardsByTyp(query);
});

function filterSensorCardsByTyp(query) {
  searchedSen = 0; // Reset the count before filtering
  const sensorsContainer = document
    .getElementById("sensors")
    .querySelector(".row");
  const cards = sensorsContainer.querySelectorAll(".card");

  cards.forEach((card) => {
    const sensorTyp = card
      .querySelector(".card-text")
      .textContent.toLowerCase(); // Assuming typ is displayed in the card text
    if (query === "" || sensorTyp.includes(query.toLowerCase())) {
      card.style.display = "block";
      searchedSen++; // Increment the count for each filtered sensor
    } else {
      card.style.display = "none";
    }
  });

  const summaryContainer = document.getElementById("summary");
  summaryContainer.querySelector("h5:nth-child(2)").textContent =
    `Počet vyhledaných senzorů: ${searchedSen}`;
}
