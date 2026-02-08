/* jshint esversion: 11 */
/* Dashboard helpers for auto-submit filters and confirm prompts. */
(() => {
  const onReady = () => {
    const autoSubmitFields = document.querySelectorAll("[data-auto-submit]");
    autoSubmitFields.forEach((field) => {
      field.addEventListener("change", () => {
        if (field.form) {
          field.form.submit();
        }
      });
    });

    const confirmTargets = document.querySelectorAll("[data-confirm]");
    confirmTargets.forEach((target) => {
      target.addEventListener("click", (event) => {
        const message = target.getAttribute("data-confirm");
        if (!message) {
          return;
        }
        if (!window.confirm(message)) {
          event.preventDefault();
          event.stopPropagation();
        }
      });
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
})();
