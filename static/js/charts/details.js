//wykres na stronę ze szczegółami wydarzenia
    var randomScalingFactor3 = function(){ return Math.round(Math.random()*100)};
    var chartDetails = {
        labels : ["22 września","23 września","24 września","25 września","26 września","27 września","28 września"],
        datasets : [
            {
                    fillColor : "rgba(0,0,0,0)",
                    strokeColor : "#fff",
                    pointColor : "#ea6a2a",
                    pointStrokeColor : "#ea6a2a",
                    pointHighlightFill : "#fff",
                    pointHighlightStroke : "rgba(220,220,220,1)",
                    data : [randomScalingFactor3(),randomScalingFactor3(),randomScalingFactor3(),randomScalingFactor3(),randomScalingFactor3(),randomScalingFactor3(),randomScalingFactor3()]
            }
        ]
    }

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

    window.onload = function(){
        
        var details = document.getElementById("chart-details").getContext("2d");
        window.myLine = new Chart(details).Line(chartDetails, {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10});
        
        var betchart1 = document.getElementById("bet-canvas01").getContext("2d");
        window.myLine = new Chart(betchart1).Line(lineChartData, {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10});
        var betchart2 = document.getElementById("bet-canvas02").getContext("2d");
        window.myLine = new Chart(betchart2).Line(lineChartData, {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10});
        var betchart3 = document.getElementById("bet-canvas03").getContext("2d");
        window.myLine = new Chart(betchart3).Line(lineChartData, {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10});
    }