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

var CHART_STYLE = {
    responsive: true,
    showScale: false,
    scaleShowLabels: false,
    datasetStrokeWidth: 6,
    bezierCurveTension: 0.5,
    pointDotRadius: 6,
    scaleOverride : true,
    scaleSteps : 10,
    scaleStepWidth: 10,
    scaleStartValue: 0,
    pointHitDetectionRadius: 10
};

var FRONT_CHART_STYLE = {
    responsive: true,
    showScale: false,
    scaleShowLabels: false,
    datasetStrokeWidth : 6,
    bezierCurveTension : 0.5,
    pointDotRadius : 6,
    scaleOverride : true,
    scaleSteps : 10,
    scaleStepWidth: 10,
    scaleStartValue: 0,
    pointHitDetectionRadius : 40
};

//wykresy na wydarzenia w betfeedzie

    
function makeChart(data,opts){

    var id = opts.id;
    var setStyle;
    if(opts && opts.setStyle){
        setStyle = opts.setStyle;
    }
    else {
        setStyle = copyObj(SET_STYLE);
    }

    var chartStyle;
    if(opts && opts.chartStyle) {
        chartStyle = opts.chartStyle;
    }
    else {
        chartStyle = CHART_STYLE;
    }

    var betCanvases = document.querySelectorAll(id);
    for (var i = 0, len = betCanvases.length; i < len; i++) {
        var chartData = {
            labels : data.labels,
            datasets : [SET_STYLE]
        };

        chartData.datasets[0].data = data.points;

        new Chart(betCanvases[i].getContext('2d')).Line(chartData,chartStyle);
    }
}

function renderCharts(events, featuredEvent, chartDetails) {
    if (events) {
        for (var i = 0, len = events.length; i < len; i++) {
            makeChart(events[i],{
                id : '.bet-'+events[i].id+'-canvas'
            });
        }
    }
    // var frontchartData = chartData;

    if(featuredEvent) {
        makeChart(featuredEvent, {
            id : '#featured-canvas',
            chartStyle: FRONT_CHART_STYLE
        });
    }

    if(chartDetails) {
        makeChart(chartDetails, {
            id : '#chart-details',
            chartStyle: FRONT_CHART_STYLE
        });
    }
}
