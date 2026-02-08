/* jshint esversion: 11 */
// Client dashboard mobile menu toggle
document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;
  const toggle = document.querySelector("[data-dashboard-toggle]");
  const sidebar = document.querySelector("[data-dashboard-sidebar]");
  const overlay = document.querySelector("[data-dashboard-overlay]");

  // Exit if not on client dashboard
  if (!toggle || !sidebar || !overlay) return;

  const setOpen = (open) => {
    body.classList.toggle("dashboard-menu-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    overlay.hidden = !open;
  };

  // Toggle on button click
  toggle.addEventListener("click", (e) => {
    e.stopPropagation();
    const isOpen = body.classList.contains("dashboard-menu-open");
    setOpen(!isOpen);
  });

  // Close on overlay click
  overlay.addEventListener("click", () => setOpen(false));

  // Close on Escape
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") setOpen(false);
  });
});
