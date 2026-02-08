/* jshint esversion: 11 */
/* Copy portal links and select inputs on click. */
(() => {
  const onReady = () => {
    const inputs = document.querySelectorAll(".portal-link-input");
    inputs.forEach((input) => {
      input.addEventListener("click", () => {
        input.select();
      });
    });

    const copyButtons = document.querySelectorAll(".portal-link-copy");
    copyButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const link = button.getAttribute("data-link") || "";
        if (!link) {
          return;
        }

        const fallbackCopy = () => {
          const temp = document.createElement("input");
          temp.value = link;
          document.body.appendChild(temp);
          temp.select();
          document.execCommand("copy");
          document.body.removeChild(temp);
        };

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(link).catch(fallbackCopy);
        } else {
          fallbackCopy();
        }

        button.textContent = "Copied";
        window.setTimeout(() => {
          button.textContent = "Copy";
        }, 1200);
      });
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
})();
