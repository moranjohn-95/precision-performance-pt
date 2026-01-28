document.addEventListener("DOMContentLoaded", function () {
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

    var labels = chartData.labels || [];
    var bodyweightData = chartData.bodyweight || [];
    var benchData = chartData.bench || [];

    function makeLineChart(canvasId, data, labelText) {
        var canvas = document.getElementById(canvasId);
        if (!canvas) return;

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
