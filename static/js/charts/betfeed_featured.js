//wykres na wyróżnione wydarzenie
//

function copyObj(obj){
    return JSON.parse(JSON.stringify(obj));
}

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
    for (var i = 0, len = chartData.length; i < len; i++) {
        makeChart(chartData[i]);
    }
    // var frontchartData = chartData;

    // var ctx = document.getElementById("featured-canvas").getContext("2d");
    // makeChart(FEATURED_chartData, {chartStyle:FEATURED_CHART_STYLE});
}
