// see also http://jsfiddle.net/GhEh9/

var chart;

function drawChart() {
    var data;
    data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', 'yläkerta temp');
    data.addColumn('string', 'yläkerta annotation');

    chart = new google.visualization.AnnotationChart(document.getElementById('chart_div'));

    var options = {
        displayAnnotations: true,
    };

    chart.draw(data, options);

    $.getJSON('https://api.thingspeak.com/channels/14421/feed.json?callback=?', function (data) {

        var data2 = new google.visualization.DataTable();
        data2.addColumn('date', 'Date');
        data2.addColumn('number', 'yläkerta temp');
        data2.addColumn('string', 'yläkerta annotation');

        var a = [];
        var dt = [];
        for (var i = 0; i < data.feeds.length; i++) {
            if (data.feeds[i].field1) {
                a.push(parseFloat(data.feeds[i].field1));
                dt.push(data.feeds[i].created_at);

            }
        }

        for (var i = 0; i < dt.length; i++) {
            data2.addRow([new Date(dt[i]), a[i], undefined]);
        }

        chart.draw(data2, {
            displayAnnotations: true,
        });
        chart.setVisibleChartRange(null, null);

    });
}

google.load('visualization', '1.1', {
    'packages': ['annotationchart']
});
google.setOnLoadCallback(drawChart);
