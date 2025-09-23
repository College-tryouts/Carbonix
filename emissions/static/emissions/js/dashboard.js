// Toggle chatbot visibility
function toggleChatbot() {
  const box = document.getElementById("chatbot-box");
  box.style.display = box.style.display === "flex" ? "none" : "flex";
}

// Show emission chart placeholder
function showEmission(pollutantId) {
  const chartArea = document.getElementById("chart-area");
  chartArea.innerHTML = `<h3>Pollutant ${pollutantId}</h3>
    <p>Here will be the time-series visualization (use Chart.js / Plotly later).</p>`;
}

// Chatbot input
const chatInput = document.getElementById("chat-input");
if (chatInput) {
  chatInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && chatInput.value.trim() !== "") {
      const content = document.getElementById("chat-content");
      content.innerHTML += `<p><strong>You:</strong> ${chatInput.value}</p>`;
      content.innerHTML += `<p><strong>Bot:</strong> I'm analyzing your emissions data...</p>`;
      chatInput.value = "";
      content.scrollTop = content.scrollHeight;
    }
  });
}
