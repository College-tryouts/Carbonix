const POLLUTANT_DATA = window.pollutantSensorData || {}; // safe fallback
const ICON_MAP = window.iconMap || {};

function getPollutantData(id) {
  return POLLUTANT_DATA[String(id)] || [];
}

function toggleChatbot() {
  const box = document.getElementById("chatbot-box");
  box.style.display = box.style.display === "flex" ? "none" : "flex";
}

function showEmission(pollutantId) {
  const chartArea = document.getElementById("chart-area");
  chartArea.innerHTML = ""; // clear old chart

  const data = getPollutantData(pollutantId);
  console.log("Drawing chart for pollutant:", pollutantId, data);

  if (!data || data.length === 0) {
    chartArea.innerHTML = "<p>No data available for this pollutant.</p>";
    return;
  }

  // Create canvas with fixed size
  const canvas = document.createElement("canvas");
  canvas.id = "pollutant-chart";
  canvas.width = 800;
  canvas.height = 400;
  chartArea.appendChild(canvas);

  // Group readings by sensor
  const sensorGroups = {};

  data.forEach(d => {
  if (!sensorGroups[d.sensor]) sensorGroups[d.sensor] = [];
  // Convert timestamp safely
  let ts = d.timestamp.split('.')[0]; // remove microseconds
  sensorGroups[d.sensor].push({ 
    x: new Date(ts), 
    y: Number(d.value) 
  });
});


  console.log("Sensor groups prepared for chart:", sensorGroups);

  const datasets = Object.keys(sensorGroups).map(sensorName => {
    const color = `hsl(${Math.random() * 360}, 70%, 55%)`;
    console.log("Dataset for sensor:", sensorName, sensorGroups[sensorName]);
    return {
      label: `${sensorName} (${data[0].unit})`,
      data: sensorGroups[sensorName],
      borderColor: color,
      backgroundColor: color + "33",
      fill: true,
      tension: 0.2
    };
  });

  // Destroy previous chart if exists
  if (window.currentChart) window.currentChart.destroy();

  window.currentChart = new Chart(canvas, {
    type: "line",
    data: { datasets: datasets },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        tooltip: { usePointStyle: true }
      },
      scales: {
        x: { type: "time", title: { display: true, text: "Time" } },
        y: { title: { display: true, text: "Value" } }
      }
    }
  });

  if (window.currentChart) {
  console.log("✅ Chart rendered successfully!");
  console.log("📊 Number of datasets:", window.currentChart.data.datasets.length);
  console.log("📈 First dataset sample:", window.currentChart.data.datasets[0]?.data.slice(0, 5));
} else {
  console.error("❌ Chart failed to initialize!");
}

}


// Pollutant click listener
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('.pollutant-card').forEach(card => {
    card.addEventListener('click', () => {
      const pollutantId = card.dataset.id;
      showEmission(pollutantId);
    });
  });
});

// Chatbot input listener
const chatInput = document.getElementById("chat-input");
if (chatInput) {
  chatInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && chatInput.value.trim() !== "") {
      const content = document.getElementById("chat-content");
      const message = chatInput.value.trim();
      const mineName = document.getElementById("mine-dashboard").dataset.mineName;

      content.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
      chatInput.value = "";

      fetch(`${CHATBOT_URL}?message=${encodeURIComponent(message)}&mine=${encodeURIComponent(mineName)}`)
        .then(res => res.json())
        .then(data => {
          content.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
          content.scrollTop = content.scrollHeight;
        })
        .catch(err => {
          content.innerHTML += `<p><strong>Bot:</strong> Sorry, error occurred.</p>`;
        });
    }
  });
}

// Menu & form toggles
function toggleMenu() {
  const menu = document.getElementById("slide-menu");
  menu.style.left = menu.style.left === "0px" ? "-500px" : "0px";
}
function toggleForm(formId) {
  const form = document.getElementById(formId);
  form.style.display = form.style.display === "none" || form.style.display === "" ? "block" : "none";
}


// const reduceBtn = document.querySelector('.reduce-btn');
// const botResponse = document.getElementById('bot-response');

// reduceBtn.addEventListener('click', () => {
//     const mineName = "{{ mine.name }}"; // Django template variable for mine
//     const userMessage = "Suggest ways to reduce emissions"; // or make dynamic later

//     // Show loading
//     botResponse.innerHTML = "Thinking... 🤔";

// fetch(`/chatbot/?mine=${encodeURIComponent(mineName)}&message=${encodeURIComponent(userMessage)}`)
//   .then(response => response.text())  // read as text first
//   .then(text => {
//       console.log("Raw response:", text); // see exactly what came back
//       try {
//           const data = JSON.parse(text);
//           botResponse.innerHTML = data.response;
//       } catch(e) {
//           botResponse.innerHTML = `Error parsing JSON: ${e.message}`;
//       }
//   });

