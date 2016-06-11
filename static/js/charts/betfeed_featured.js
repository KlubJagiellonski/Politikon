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
    pointHitDetectionRadius: 3
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
    pointHitDetectionRadius: 5
};

//wykresy na wydarzenia w betfeedzie

    
function makeChart(obj, opts){

    var id = opts.id;
    var setStyle;
    var data = $(obj).data('chart');

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

    var chartData = {
        labels : data.labels,
        datasets : [SET_STYLE]
    };
    chartData.datasets[0].data = data.points;

    new Chart(document.getElementById(id).getContext('2d')).Line(chartData, chartStyle);
}

function renderCharts() {
    $(".event-canvas[data-chart]").each(function (i, x) {
        makeChart(x, {
            id : 'event-' + $(x).data('id') + '-canvas'
        });
    });

    var featuredEvent = document.getElementById('featured-canvas');
    if(featuredEvent) {
        makeChart(featuredEvent, {
            id : 'featured-canvas',
            chartStyle: FRONT_CHART_STYLE
        });
    }

    var chartDetails = document.getElementById('chart-details');
    if(chartDetails) {
        makeChart(chartDetails, {
            id : 'chart-details',
            chartStyle: FRONT_CHART_STYLE
        });
    }
}

$(function() {
    renderCharts();
});