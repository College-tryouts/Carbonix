// Toggle chatbot
function toggleChatbot() {
  const box = document.getElementById("chatbot-box");
  box.style.display = box.style.display === "flex" ? "none" : "flex";
}

function showEmission(pollutantId) {
    const chartArea = document.getElementById("chart-area");
    const data = emissionsData[String(pollutantId)]; // ✅ match string keys

    if (data && data.length > 0) {
        chartArea.innerHTML = `<canvas id="emissionChart"></canvas>`;
        renderChart(
            data.map(d => ({ timestamp: d.period_start, value: d.emission_value })),
            'kg'
        );
    } else {
        chartArea.innerHTML = "<p>Data not available for this pollutant.</p>";
    }
}
// Chart.js colorful + animated chart
function renderChart(values, unit) {
    const ctx = document.getElementById('emissionChart').getContext('2d');

    // Rainbow gradient for line
    const gradientLine = ctx.createLinearGradient(0, 0, ctx.canvas.width, 0);
    gradientLine.addColorStop(0, '#ff4e50');
    gradientLine.addColorStop(0.25, '#fc913a');
    gradientLine.addColorStop(0.5, '#f9d423');
    gradientLine.addColorStop(0.75, '#24c6dc');
    gradientLine.addColorStop(1, '#5433ff');

    // Gradient background fill
    const gradientFill = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height);
    gradientFill.addColorStop(0, 'rgba(84,51,255,0.4)');
    gradientFill.addColorStop(1, 'rgba(36,198,220,0.05)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: values.map(v => v.timestamp),
            datasets: [{
                label: `Emission (${unit})`,
                data: values.map(v => v.value),
                borderColor: gradientLine,
                borderWidth: 3,
                backgroundColor: gradientFill,
                pointBackgroundColor: values.map((_, i) =>
                    i % 2 === 0 ? '#ff4e50' : '#24c6dc'
                ),
                pointBorderColor: '#fff',
                pointRadius: 8,
                pointHoverRadius: 12,
                pointHoverBackgroundColor: '#f9d423',
                fill: true,
                tension: 0.5
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: '#fff', font: { size: 14 } }
                },
                tooltip: {
                    backgroundColor: '#222',
                    titleColor: '#00e6e6',
                    bodyColor: '#fff',
                    usePointStyle: true
                }
            },
            interaction: { mode: 'nearest', intersect: false },
            scales: {
                x: { ticks: { color: '#ccc' }, grid: { color: '#444' } },
                y: { ticks: { color: '#ccc' }, grid: { color: '#444' } }
            },
            animation: {
                duration: 2500,
                easing: 'easeOutElastic',
                delay: (context) => context.dataIndex * 200
            }
        }
    });
}



document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('.pollutant-card').forEach(card => {
    card.addEventListener('click', () => {
      const pollutantId = card.dataset.id;
      showEmission(pollutantId);
    });
  });
});




// Existing code for chart rendering and pollutant clicks
// ...

// Chatbot input listener
const chatInput = document.getElementById("chat-input");
if(chatInput){
  chatInput.addEventListener("keypress", function(e){
    if(e.key === "Enter" && chatInput.value.trim() !== ""){
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


function toggleMenu() {
  const menu = document.getElementById("slide-menu");
  if (menu.style.left === "0px") {
    menu.style.left = "-500px";
  } else {
    menu.style.left = "0px";
  }
}


function toggleForm(formId) {
  const form = document.getElementById(formId);
  if (form.style.display === "none" || form.style.display === "") {
    form.style.display = "block";
  } else {
    form.style.display = "none";
  }
}
