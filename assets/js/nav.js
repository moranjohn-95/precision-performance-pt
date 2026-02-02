// Burger menu toggle for the public navbar only
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const menu = document.querySelector(".nav-menu");

  // Exit quietly if this page doesn't have the public navbar
  if (!toggle || !menu) return;

  const setOpen = (open) => {
    menu.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  };

  // Toggle the menu on burger click
  toggle.addEventListener("click", (e) => {
    e.stopPropagation();
    const isOpen = menu.classList.contains("is-open");
    setOpen(!isOpen);
  });

  // Close when clicking outside the menu
  document.addEventListener("click", () => setOpen(false));

  // Keep clicks inside the menu from closing it immediately
  menu.addEventListener("click", (e) => e.stopPropagation());

  // Close after clicking any link inside the menu
  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => setOpen(false));
  });

  // Close on Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") setOpen(false);
  });
});
