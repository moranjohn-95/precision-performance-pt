// Program details modal
(function () {
  const modal = document.querySelector("[data-program-modal]");
  const overlay = document.querySelector("[data-program-modal-overlay]");
  const closeBtn = document.querySelector("[data-program-modal-close]");
  const triggers = document.querySelectorAll("[data-program-trigger]");

  if (!modal || !overlay || !closeBtn || triggers.length === 0) {
    return;
  }

  function openModal() {
    overlay.classList.add("is-open");
    modal.classList.add("is-open");
  }

  function closeModal() {
    overlay.classList.remove("is-open");
    modal.classList.remove("is-open");
  }

  triggers.forEach((btn) => {
    btn.addEventListener("click", (event) => {
      event.preventDefault();
      openModal();
    });
  });

  closeBtn.addEventListener("click", closeModal);
  overlay.addEventListener("click", closeModal);
})();
