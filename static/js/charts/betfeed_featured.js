//wykres na wyróżnione wydarzenie
//

var randomScalingFactor = function(){ return Math.round(Math.random()*100)};
var randomScalingFactor2 = function(){ return Math.round(Math.random()*75)};

function copyObj(obj){
    return JSON.parse(JSON.stringify(obj));
}

var chartDataEx = {
    labels : ["22 września","23 września","24 września","25 września","26 września","27 września","28 września"],
    points : [randomScalingFactor2(),randomScalingFactor2(),randomScalingFactor2(),randomScalingFactor2(),randomScalingFactor2(),randomScalingFactor2(),randomScalingFactor2() ]
};


var SET_STYLE = {
    fillColor : "rgba(0,0,0,0)",
    strokeColor : "#fff",
    pointColor : "#ea6a2a",
    pointStrokeColor : "#ea6a2a",
    pointHighlightFill : "#fff",
    pointHighlightStroke : "rgba(220,220,220,1)"
};

var CHART_STYLE = {responsive: true,showScale: false,scaleShowLabels: false,datasetStrokeWidth : 6,bezierCurveTension : 0.5,pointDotRadius : 6,pointHitDetectionRadius : 10};

var FEATURED_CHART_STYLE = { responsive: true,showScale: false, scaleShowLabels: false, datasetStrokeWidth : 6, bezierCurveTension : 0.5, pointDotRadius : 6, pointHitDetectionRadius : 40};

//wykresy na wydarzenia w betfeedzie

function makeChart(data,opts){
    var id = 'bet-'+data.id+'-canvas';

    var setStyle;
    if(opts && opts.setStyle){
        setStyle = opts.setStyle;
    }else{
        setStyle = copyObj(SET_STYLE);
    }

    var chartStyle;
    if(opts && opts.chartStyle){
        chartStyle = opts.chartStyle;
    }else{
        chartStyle = CHART_STYLE;
    }

    var betCanvas = document.getElementById(id).getContext("2d");
    var chartData = {
        labels : data.labels,
        datasets : [SET_STYLE]
    };

    chartData.datasets[0].data = data.points;

    new Chart(betCanvas).Line(chartData,chartStyle);
}

function renderCharts(chartData){
    console.log(chartData);
    chartData = (function() {
        for (var i = 0, len = chartData.length; i < len; i++) {
            $.extend(chartData[i],chartDataEx);
        }
        return chartData;

    }());

    var FEATURED_chartData = chartData;
    for (var i = 0, len = chartData.length; i < len; i++) {
        var data = chartData[i];
        makeChart(data);
    }

    // var ctx = document.getElementById("featured-canvas").getContext("2d");
    // makeChart(FEATURED_chartData, {chartStyle:FEATURED_CHART_STYLE});
}
