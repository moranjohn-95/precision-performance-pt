/* jshint esversion: 11 */
/* Enable the assign button when a trainer is selected. */
(() => {
  const onReady = () => {
    const select = document.querySelector("[data-assign-toggle]");
    if (!select) {
      return;
    }

    const targetId = select.getAttribute("data-assign-target");
    const target = targetId ? document.getElementById(targetId) : null;
    if (!target) {
      return;
    }

    const updateState = () => {
      target.disabled = !select.value;
    };

    select.addEventListener("change", updateState);
    updateState();
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
})();
