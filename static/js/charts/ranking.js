//wykres na ranking zalogowanego
function rankingChart(data) {
    var rankingChartData = {
        labels: data.labels,
        datasets: [
            {
                fillColor: "#58585a",
                strokeColor: "#ea6a2a",
                pointColor: "#fff",
                pointStrokeColor: "#ea6a2a",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: data.points
            }
        ]
    };

    window.onload = function betfeed() {
        var ctx = document.getElementById("ranking-canvas").getContext("2d");
        window.myLine = new Chart(ctx).Line(rankingChartData, {
            responsive: true,
            showScale: false,
            scaleShowLabels: false,
            datasetStrokeWidth: 6,
            bezierCurveTension: 0.5,
            pointDotRadius: 6,
            pointHitDetectionRadius: 40
        });
    }
}