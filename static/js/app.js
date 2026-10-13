const modal = document.getElementById("detail-modal");
const closeButton = document.getElementById("close-modal");
let activeConcept = null;

function showToast(message) {
  const old = document.querySelector(".toast");
  if (old) old.remove();
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 2200);
}

function setText(id, value) {
  document.getElementById(id).textContent = value || "Información no disponible.";
}

async function openConcept(id) {
  try {
    const response = await fetch(`/api/conceptos/${id}`);
    if (!response.ok) throw new Error("No se encontró el concepto.");
    const c = await response.json();
    activeConcept = c;
    setText("detail-title", c.nombre);
    setText("detail-category", c.categoria);
    setText("detail-summary", c.resumen);
    setText("detail-description", c.descripcion);
    setText("detail-functions", c.funciones);
    setText("detail-location", c.ubicacion);
    const facts = document.getElementById("detail-facts");
    facts.replaceChildren();
    (c.curiosidades || "").split("\n").filter(Boolean).forEach(fact => {
      const li = document.createElement("li");
      li.textContent = fact;
      facts.appendChild(li);
    });
    const image = document.getElementById("detail-image");
    const emoji = document.getElementById("detail-emoji");
    image.hidden = true;
    image.onerror = () => { image.hidden = true; emoji.hidden = false; };
    if (c.imagen_url) {
      image.src = c.imagen_url;
      image.alt = `Ilustración de ${c.nombre}`;
      image.onload = () => { image.hidden = false; emoji.hidden = true; };
    }
    emoji.textContent = c.emoji || "🔬";
    emoji.hidden = false;
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    closeButton.focus();
  } catch (error) {
    showToast("No se pudo cargar la ficha. Intenta de nuevo.");
  }
}

document.querySelectorAll(".concept-card").forEach(card => {
  card.addEventListener("click", () => openConcept(card.dataset.id));
});
function closeModal() {
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
}
closeButton.addEventListener("click", closeModal);
modal.addEventListener("click", event => { if (event.target === modal) closeModal(); });
document.addEventListener("keydown", event => { if (event.key === "Escape") closeModal(); });
document.getElementById("copy-detail").addEventListener("click", async () => {
  if (!activeConcept) return;
  const c = activeConcept;
  const text = `${c.nombre}\nCategoría: ${c.categoria}\n\nDescripción:\n${c.descripcion}\n\nFunciones:\n${c.funciones}\n\nDatos curiosos:\n${c.curiosidades}\n\nUbicación: ${c.ubicacion}`;
  try {
    await navigator.clipboard.writeText(text);
    showToast("¡Ficha copiada al portapapeles!");
  } catch {
    showToast("Tu navegador no permitió copiar la ficha.");
  }
});
