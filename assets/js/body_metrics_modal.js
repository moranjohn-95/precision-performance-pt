document.addEventListener("DOMContentLoaded", function () {
    const backdrop = document.getElementById("metrics-modal-backdrop");
    if (!backdrop) return;

    const idField = document.getElementById("metric-entry-id");
    const dateField = document.getElementById("metric-date");
    const bodyweightField = document.getElementById("metric-bodyweight");
    const waistField = document.getElementById("metric-waist");
    const benchField = document.getElementById("metric-bench");
    const sleepField = document.getElementById("metric-sleep");
    const notesField = document.getElementById("metric-notes");

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

    function closeModal() {
        backdrop.classList.add("is-hidden");
        document.body.classList.remove("no-scroll");
    }

    document.querySelectorAll(".js-open-metric").forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            openModalFromLink(link);
        });
    });

    document
        .querySelectorAll(".js-close-metric")
        .forEach(function (btn) {
            btn.addEventListener("click", function (event) {
                event.preventDefault();
                closeModal();
            });
        });

    backdrop.addEventListener("click", function (event) {
        if (event.target === backdrop) {
            closeModal();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && !backdrop.classList.contains("is-hidden")) {
            closeModal();
        }
    });
});
