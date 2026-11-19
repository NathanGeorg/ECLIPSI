const API = "http://127.0.0.1:8000";
let token = null;

document.querySelector("#login").addEventListener("click", async () => {
  const result = document.querySelector("#loginResult");
  result.textContent = "Entrando...";
  try {
    const response = await fetch(`${API}/api/auth/login`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        email: document.querySelector("#email").value,
        password: document.querySelector("#password").value
      })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Falha no login");
    token = data.access_token;
    result.textContent = `Conectado como ${data.name} (${data.role})`;
  } catch (error) {
    result.textContent = error.message;
    result.className = "error";
  }
});

document.querySelector("#search").addEventListener("click", async () => {
  const specialty = document.querySelector("#specialty").value;
  const container = document.querySelector("#professionals");
  container.textContent = "Buscando...";
  const response = await fetch(`${API}/api/professionals${specialty ? `?specialty=${encodeURIComponent(specialty)}` : ""}`);
  const data = await response.json();
  container.textContent = "";
  if (!response.ok) {
    container.textContent = data.detail || "Erro na busca";
    return;
  }
  data.forEach(item => {
    const card = document.createElement("div");
    card.className = "card";
    card.textContent = `${item.name} — ${item.specialty}, ${item.modality}, R$ ${item.price}`;
    container.appendChild(card);
  });
});
