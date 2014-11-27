//wykres na ranking zalogowanego
    var randomScalingFactor = function(){ return Math.round(Math.random()*100)};
    var rankingChartData = {
        labels : ["22 września","23 września","24 września","25 września","26 września","27 września","28 września"],
        datasets : [
            {
                    fillColor : "#58585a",
                    strokeColor : "#ea6a2a",
                    pointColor : "#fff",
                    pointStrokeColor : "#ea6a2a",
                    pointHighlightFill : "#fff",
                    pointHighlightStroke : "rgba(220,220,220,1)",
                    data : [randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor()]
            }
        ]
    }

    window.onload = function betfeed(){
        var ctx = document.getElementById("ranking-canvas").getContext("2d");
        window.myLine = new Chart(ctx).Line(rankingChartData, { responsive: true,showScale: false, scaleShowLabels: false, datasetStrokeWidth : 6, bezierCurveTension : 0.5, pointDotRadius : 6, pointHitDetectionRadius : 40});
}
