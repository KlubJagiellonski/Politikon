//wykres na profil uzytkownika
    var randomScalingFactor = function(){ return Math.round(Math.random()*100)};
    var profileChartData = {
        labels : ["22 września","23 września","24 września","25 września","26 września","27 września","28 września"],
        datasets : [
            {
                    fillColor : "#ea6a2a",
                    strokeColor : "#fff",
                    pointColor : "#fff",
                    pointStrokeColor : "#ea6a2a",
                    pointHighlightFill : "#fff",
                    pointHighlightStroke : "rgba(220,220,220,1)",
                    data : [randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor()]
            }
        ]
    }

    window.onload = function betfeed(){
        var ctx = document.getElementById("profile-canvas").getContext("2d");
        window.myLine = new Chart(ctx).Line(profileChartData, { responsive: true,showScale: false, scaleShowLabels: false, datasetStrokeWidth : 6, bezierCurveTension : 0.5, pointDotRadius : 6, pointHitDetectionRadius : 40});
}
