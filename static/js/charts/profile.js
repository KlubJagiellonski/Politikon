//wykres na profil uzytkownika
function profileChart(data) {
    if (data) {
        var profileChartData = {
            labels: data.labels,
            datasets: [
                {
                    fillColor: "#ea6a2a",
                    strokeColor: "#fff",
                    pointColor: "#fff",
                    pointStrokeColor: "#ea6a2a",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(220,220,220,1)",
                    data: data.points
                }
            ]
        };

        window.onload = function betfeed() {
            var ctx = document.getElementById("profile-canvas").getContext("2d");
            window.myLine = new Chart(ctx).Line(profileChartData, {
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
}
