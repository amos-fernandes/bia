const API_BASE_URL = "http://192.168.1.47:5000/api"; // ajuste se necessário

export async function getConnectionStatus() {
  const res = await fetch(`${API_BASE_URL}/status`);
  if (!res.ok) throw new Error("Erro ao buscar status");
  return res.json();
}

export interface Settings {
  // Define the expected properties of settings here
  // For example:
  // username: string;
  // password: string;
  // host: string;
  // port: number;
  [key: string]: unknown;
}

export async function saveSettings(settings: Settings) {
  const res = await fetch(`${API_BASE_URL}/settings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(settings),
  });
  if (!res.ok) throw new Error("Erro ao salvar configurações");
  return res.json();
}

export async function testConnections() {
  const res = await fetch(`${API_BASE_URL}/test-connections`);
  if (!res.ok) throw new Error("Erro ao testar conexões");
  return res.json();
}
