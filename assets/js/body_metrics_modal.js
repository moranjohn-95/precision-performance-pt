/* jshint esversion: 11 */
/* Body metrics modal for client and trainer metrics pages. */
document.addEventListener("DOMContentLoaded", function () {
    // DOM lookups for the modal and its fields.
    const backdrop = document.getElementById("metrics-modal-backdrop");
    if (!backdrop) return;

    const idField = document.getElementById("metric-entry-id");
    const dateField = document.getElementById("metric-date");
    const bodyweightField = document.getElementById("metric-bodyweight");
    const waistField = document.getElementById("metric-waist");
    const benchField = document.getElementById("metric-bench");
    const sleepField = document.getElementById("metric-sleep");
    const notesField = document.getElementById("metric-notes");

    // Helper to populate the form from data attributes on a trigger link.
    function openModalFromLink(link) {
        idField.value = link.dataset.entryId || "";
        dateField.value = link.dataset.date || "";
        bodyweightField.value = link.dataset.bodyweight || "";
        waistField.value = link.dataset.waist || "";
        benchField.value = link.dataset.bench || "";
        sleepField.value = link.dataset.sleep || "";
        notesField.value = link.dataset.notes || "";

        backdrop.classList.remove("is-hidden");
        document.body.classList.add("no-scroll");
    }

    // Helper to reset the UI state and close the modal.
    function closeModal() {
        backdrop.classList.add("is-hidden");
        document.body.classList.remove("no-scroll");
    }

    // Open modal from a session row link.
    document.querySelectorAll(".js-open-metric").forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            openModalFromLink(link);
        });
    });

    // Close modal from any close control.
    document
        .querySelectorAll(".js-close-metric")
        .forEach(function (btn) {
            btn.addEventListener("click", function (event) {
                event.preventDefault();
                closeModal();
            });
        });

    // Close when clicking the backdrop itself.
    backdrop.addEventListener("click", function (event) {
        if (event.target === backdrop) {
            closeModal();
        }
    });

    // Close on Escape for keyboard users.
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && !backdrop.classList.contains("is-hidden")) {
            closeModal();
        }
    });
});
