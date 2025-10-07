async function loadJSON(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`No se pudo cargar ${url}`);
  return r.json();
}

function statusBadgeStock(row) {
  if (row.stock_min === undefined) return "";
  const ok = row.stock >= row.stock_min;
  return `<span class="badge ${ok ? "bg-success" : "bg-danger"}">
    ${ok ? "OK" : "Bajo"}
  </span>`;
}

function severidadBadge(s) {
  const map = { "ALTA": "bg-danger", "MEDIA": "bg-warning text-dark", "BAJA": "bg-success" };
  return `<span class="badge ${map[s] || "bg-secondary"}">${s}</span>`;
}

function tipoMovBadge(t) {
  const map = { "ENTRADA": "bg-success", "SALIDA": "bg-primary", "AJUSTE": "bg-secondary" };
  return `<span class="badge ${map[t] || "bg-light text-dark"}">${t}</span>`;
}

function daysUntil(dateStr) {
  if (!dateStr) return null;
  const d = new Date(dateStr + "T00:00:00");
  const now = new Date();
  return Math.ceil((d - now) / (1000*60*60*24));
}

function caducidadPill(dateStr) {
  if (!dateStr) return `<span class="badge bg-secondary">—</span>`;
  const dLeft = daysUntil(dateStr);
  let cls = "bg-success";
  if (dLeft <= 15) cls = "bg-danger";
  else if (dLeft <= 30) cls = "bg-warning text-dark";
  return `<span class="badge ${cls}">${dateStr} (${dLeft} días)</span>`;
}

function simpleSearch(inputEl, tableEl) {
  inputEl.addEventListener("input", () => {
    const q = inputEl.value.toLowerCase();
    tableEl.querySelectorAll("tbody tr").forEach(tr => {
      tr.style.display = tr.textContent.toLowerCase().includes(q) ? "" : "none";
    });
  });
}

window.SecretoUI = {
  loadJSON, statusBadgeStock, severidadBadge, tipoMovBadge, caducidadPill, simpleSearch
};
