export async function validateRequest(payload: any) {
  const res = await fetch("http://localhost:8000/v1/json-request/validate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function normalizeRequest(payload: any) {
  const res = await fetch("http://localhost:8000/v1/json-request/normalize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function saveRequest(payload: any) {
  const res = await fetch("http://localhost:8000/v1/json-request/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function sendToBlackbox(id: number) {
  const res = await fetch(`http://localhost:8000/v1/json-request/${id}/send`, {
    method: "POST",
  });
  return res.json();
}

export async function getRequest(id: number) {
  const res = await fetch(`http://localhost:8000/v1/json-request/${id}`);
  return res.json();
}

export async function getLogs(id: number) {
  const res = await fetch(`http://localhost:8000/v1/json-request/${id}/logs`);
  return res.json();
}