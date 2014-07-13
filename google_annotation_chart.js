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

        var data_field1 = new google.visualization.DataTable();
        data_field1.addColumn('date', 'Date');
        data_field1.addColumn('number', 'yläkerta temp');
        data_field1.addColumn('string', 'yläkerta annotation');

        var data_field2 = new google.visualization.DataTable();
        data_field2.addColumn('date', 'Date');
        data_field2.addColumn('number', 'alakerta temp');
        data_field2.addColumn('string', 'alakerta annotation');

        var data_field3 = new google.visualization.DataTable();
        data_field3.addColumn('date', 'Date');
        data_field3.addColumn('number', 'ulko temp');
        data_field3.addColumn('string', 'ulko annotation');

        var currentFeed;
        for (var i = 0; i < data.feeds.length; i++) {
            currentFeed = data.feeds[i];
            if (currentFeed.field1) {
                data_field1.addRow([new Date(currentFeed.created_at), parseFloat(currentFeed.field1), undefined]);
            }
        }
        for (var i = 0; i < data.feeds.length; i++) {
            currentFeed = data.feeds[i];
            if (currentFeed.field2) {
                data_field2.addRow([new Date(currentFeed.created_at), parseFloat(currentFeed.field2), undefined]);
            }
        }
        for (var i = 0; i < data.feeds.length; i++) {
            currentFeed = data.feeds[i];

            if (currentFeed.field3) {
                data_field3.addRow([new Date(currentFeed.created_at), parseFloat(currentFeed.field3), undefined]);
            }
        }

    

    var data2 = google.visualization.data.join(data_field1, data_field2, 'full', [
        [0, 0]
    ], [1, 2], [1, 2]);

    chart.draw(data2, {
        displayAnnotations: true,
        interpolateNulls: true
    });
    chart.setVisibleChartRange(null, null);

    });
}

google.load('visualization', '1.1', {
    'packages': ['annotationchart']
});
google.setOnLoadCallback(drawChart);
