var  chart2;
$(document).ready(function() {
chart2 = new Highcharts.Chart({
chart: {
renderTo: 'chart_2',
plotBackgroundColor: null,
plotBorderWidth: null,
plotShadow: false,
height: 500,
},
title: {
text: 'community '
},
tooltip: {
pointFormat: '<b>{point.percentage}%</b>',
percentageDecimals: 1
},
plotOptions: {
pie: {
allowPointSelect: true,
cursor: 'pointer',
dataLabels: {
enabled: false
},
showInLegend: true
}
},
series: [{
type: 'pie',
name: 'Dev #1',
data: [
['com1',16],
['com2',15],
['com3',14],
['com4',12],
['com5',11],
['com6',10],
['com7',10],
['com8',9],
['com9',9],
['com10',9],
]
}]
});
});