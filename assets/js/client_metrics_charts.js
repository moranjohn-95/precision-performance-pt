// Render client body metrics charts from data attributes
// Keeps globals clean via an IIFE
(() => {
    // Helper: safe JSON parse
    const safeParse = (raw) => {
        try {
            return JSON.parse(raw);
        } catch (e) {
            return [];
        }
    };

    document.addEventListener("DOMContentLoaded", () => {
        // Require Chart.js
        if (typeof Chart === "undefined") return;

        const dataEl = document.getElementById("metrics-charts-data");
        if (!dataEl) return;

        const labels = safeParse(dataEl.dataset.labels || "[]");
        const bodyweightData = safeParse(dataEl.dataset.bodyweight || "[]");
        const benchData = safeParse(dataEl.dataset.bench || "[]");

        // Exit if no labels
        if (!Array.isArray(labels) || !labels.length) return;

        const makeLineChart = (canvasId, data, labelText) => {
            const canvas = document.getElementById(canvasId);
            if (!canvas) return;
            const hasValues = Array.isArray(data) && data.some((v) => v !== null);
            if (!hasValues) return;

            new Chart(canvas, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: labelText,
                            data: data,
                            tension: 0.35,
                            pointRadius: 3,
                            borderWidth: 2,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                    },
                    scales: {
                        x: { title: { display: false } },
                        y: { beginAtZero: false },
                    },
                },
            });
        };

        makeLineChart("bodyweightChart", bodyweightData, "Bodyweight (kg)");
        makeLineChart("strengthChart", benchData, "Bench top set (kg)");
    });
})();
