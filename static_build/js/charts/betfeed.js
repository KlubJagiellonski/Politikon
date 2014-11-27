//wykresy na wydarzenia w betfeedzie
    var randomScalingFactor2 = function(){ return Math.round(Math.random()*75)};
    var lineChartData = {
        labels : ["22 września","23 września","24 września","25 września","26 września","27 września","28 września"],
        datasets : [
            {
                    fillColor : "rgba(0,0,0,0)",
                    strokeColor : "#fff",
                    pointColor : "#ea6a2a",
                    pointStrokeColor : "#ea6a2a",
                    pointHighlightFill : "#fff",
                    pointHighlightStroke : "rgba(220,220,220,1)",
                    data : [randomScalingFactor2(),randomScalingFactor2(),randomScalingFactor2(),randomScalingFactor2(),randomScalingFactor2(),randomScalingFactor2(),randomScalingFactor2()]
            }
        ]
    }

    window.onload = function betfeed(){
        
        var betchart1 = document.getElementById("bet-canvas01").getContext("2d");
        window.myLine = new Chart(betchart1).Line(lineChartData, {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10});
        var betchart2 = document.getElementById("bet-canvas02").getContext("2d");
        window.myLine = new Chart(betchart2).Line(lineChartData, {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10});
        var betchart3 = document.getElementById("bet-canvas03").getContext("2d");
        window.myLine = new Chart(betchart3).Line(lineChartData, {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10});
        var betchart4 = document.getElementById("bet-canvas04").getContext("2d");
        window.myLine = new Chart(betchart4).Line(lineChartData, {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10});
        var betchart5 = document.getElementById("bet-canvas05").getContext("2d");
        window.myLine = new Chart(betchart5).Line(lineChartData, {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10});
        var betchart6 = document.getElementById("bet-canvas06").getContext("2d");
        window.myLine = new Chart(betchart6).Line(lineChartData, {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10});
        var betchart7 = document.getElementById("bet-canvas07").getContext("2d");
        window.myLine = new Chart(betchart7).Line(lineChartData, {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10});
        var betchart8 = document.getElementById("bet-canvas08").getContext("2d");
        window.myLine = new Chart(betchart8).Line(lineChartData, {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10});
        var betchart9 = document.getElementById("bet-canvas09").getContext("2d");
        window.myLine = new Chart(betchart9).Line(lineChartData, {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10});
}
