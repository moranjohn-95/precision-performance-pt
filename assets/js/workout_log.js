/* jshint esversion: 11 */
/* Workout log helpers for the client workout log page. */
(() => {
    document.addEventListener("DOMContentLoaded", function () {
        // DOM lookups for the session modal.
        const backdrop = document.getElementById("session-modal-backdrop");
        const titleEl = document.getElementById("session-modal-title");
        const idField = document.getElementById("session-id-field");
        const nameField = document.getElementById("session-name-field");
        const statusField = document.getElementById("session-status-field");
        const notesField = document.getElementById("session-notes-field");
        if (
            !backdrop ||
            !titleEl ||
            !idField ||
            !nameField ||
            !statusField ||
            !notesField
        ) {
            return;
        }

        // Fill the modal fields using row data attributes.
        function openModalFromRow(row) {
            const sessionId = row.dataset.sessionId;
            const sessionName = row.dataset.sessionName || "";
            const sessionStatus = row.dataset.sessionStatus || "logged";
            const sessionNotes = row.dataset.sessionNotes || "";

            idField.value = sessionId;
            nameField.value = sessionName;
            statusField.value = sessionStatus;
            notesField.value = sessionNotes;

            titleEl.textContent = sessionName || "Workout session";

            backdrop.classList.remove("is-hidden");
            document.body.classList.add("no-scroll");
        }

        // Close the modal and restore page scroll.
        function closeModal() {
            backdrop.classList.add("is-hidden");
            document.body.classList.remove("no-scroll");
        }

        // Open modal from the "Open" link in the session list.
        document.querySelectorAll(".js-open-session").forEach(function (btn) {
            btn.addEventListener("click", function (event) {
                event.preventDefault();
                const row = btn.closest("tr");
                if (row) {
                    openModalFromRow(row);
                }
            });
        });

        // Close modal from any close control.
        document.querySelectorAll(".js-close-session").forEach(function (btn) {
            btn.addEventListener("click", closeModal);
        });

        // Close when clicking the backdrop itself.
        backdrop.addEventListener("click", function (event) {
            if (event.target === backdrop) {
                closeModal();
            }
        });

        // Close on Escape for keyboard users.
        document.addEventListener("keydown", function (event) {
            if (
                event.key === "Escape" &&
                !backdrop.classList.contains("is-hidden")
            ) {
                closeModal();
            }
        });

        // Sync the legacy hidden set fields from the "sets x reps" input.
        const workoutRows = document.querySelectorAll(
            ".workout-row[data-ex-id]"
        );

        // Parse the "sets x reps" input with fallback to template targets.
        const parseSetsReps = (raw, fallbackSets, fallbackReps) => {
            if (!raw) return { sets: fallbackSets || 0, reps: fallbackReps || 0 };
            const cleaned = raw.toLowerCase().replace("Ã—", "x");
            const match = cleaned.match(/(\d+)\s*x\s*(\d+)/);
            if (match) {
                return {
                    sets: parseInt(match[1], 10),
                    reps: parseInt(match[2], 10),
                };
            }
            return { sets: fallbackSets || 0, reps: fallbackReps || 0 };
        };

        workoutRows.forEach((row) => {
            // Data attributes keep the template and JS in sync.
            const exId = row.dataset.exId;
            const targetSets = parseInt(row.dataset.targetSets || "0", 10);
            const targetReps = parseInt(row.dataset.targetReps || "0", 10);
            const targetWeight = row.dataset.targetWeight || "";

            const setsRepsInput = row.querySelector(
                `input[name="ex_${exId}_sets_reps"]`
            );
            const weightInput = row.querySelector(
                `input[name="ex_${exId}_weight"]`
            );
            const legacyInputs = row.querySelectorAll(".js-legacy-set");

            // Use the programme defaults if no values are entered yet.
            if (weightInput && !weightInput.value && targetWeight) {
                weightInput.value = targetWeight;
            }

            if (setsRepsInput && !setsRepsInput.value && targetSets && targetReps) {
                setsRepsInput.value = `${targetSets} x ${targetReps}`;
            }

            // Update the legacy hidden inputs on each change.
            const syncLegacy = () => {
                const parsed = parseSetsReps(
                    setsRepsInput ? setsRepsInput.value : "",
                    targetSets,
                    targetReps
                );
                legacyInputs.forEach((hidden) => {
                    const setNum = parseInt(hidden.dataset.set || "0", 10);
                    if (setNum >= 1 && setNum <= parsed.sets && parsed.reps) {
                        hidden.value = parsed.reps;
                    } else {
                        hidden.value = "";
                    }
                });
            };

            if (setsRepsInput) {
                setsRepsInput.addEventListener("input", syncLegacy);
            }
            syncLegacy();
        });

        // Stack exercise name words on smaller screens for readability.
        const exerciseEls = document.querySelectorAll(
            ".workout-cell--exercise strong"
        );
        const mq = window.matchMedia("(max-width: 992px)");

        const updateExerciseWrap = () => {
            exerciseEls.forEach((el) => {
                // Store the original text so it can be restored.
                if (!el.dataset.originalText) {
                    el.dataset.originalText = el.textContent.trim();
                }
                const original = el.dataset.originalText;
                if (!original) return;

                if (mq.matches) {
                    el.innerHTML = original.split(/\s+/).join("<br>");
                } else {
                    el.textContent = original;
                }
            });
        };

        updateExerciseWrap();
        mq.addEventListener("change", updateExerciseWrap);
    });
})();
