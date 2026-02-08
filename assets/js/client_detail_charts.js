/* jshint esversion: 11 */
/* global Chart */
/* Client metrics charts for the trainer client detail page. */
document.addEventListener("DOMContentLoaded", function () {
    // Pull chart data from the embedded JSON script tag.
    var dataScript = document.getElementById("clientChartData");
    if (!dataScript) {
        return;
    }

    var chartData;
    try {
        chartData = JSON.parse(dataScript.textContent);
    } catch (e) {
        console.error("Invalid chart data JSON", e);
        return;
    }

    // Normalize series arrays to avoid undefined values.
    var labels = chartData.labels || [];
    var bodyweightData = chartData.bodyweight || [];
    var benchData = chartData.bench || [];

    // Build a single-series line chart when data exists.
    function makeLineChart(canvasId, data, labelText) {
        var canvas = document.getElementById(canvasId);
        if (!canvas) return;

        // Skip empty datasets to avoid blank charts.
        var hasValues =
            Array.isArray(data) &&
            data.some(function (v) {
                return v !== null && v !== undefined;
            });
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
                plugins: { legend: { display: false } },
                scales: {
                    x: { title: { display: false } },
                    y: { beginAtZero: false },
                },
            },
        });
    }

    // Only draw charts when labels exist for the x-axis.
    if (Array.isArray(labels) && labels.length) {
        makeLineChart(
            "bodyweightChart",
            bodyweightData,
            "Bodyweight (kg)"
        );
        makeLineChart(
            "strengthChart",
            benchData,
            "Bench top set (kg)"
        );
    }
});
