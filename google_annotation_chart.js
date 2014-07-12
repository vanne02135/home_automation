
var chart; 

function drawChart() {
    var data;
    data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', 'yläkerta temp');
    data.addColumn('string', 'yläkerta annotation');

    data.addRows([
        [new Date(2314, 2, 15), 25, "semmosta"],
        [new Date(2314, 2, 16), 28, "tommosta"],
        [new Date(2314, 2, 17), 10, "oho"]


    ]);


    chart = new google.visualization.AnnotationChart(document.getElementById('chart_div'));

    var options = {
        displayAnnotations: true,
    };

    chart.draw(data, options);

    $.getJSON('https://api.thingspeak.com/channels/14421/feed.json?callback=?', function (data) {

        // get the data point
        p = data.field1;
        if (p) {
            p = Math.round((p / 1023) * 100);
            //displayData(p);
        }

        var data2 = new google.visualization.DataTable();
        data2.addColumn('date', 'Date');
        data2.addColumn('number', 'yläkerta temp');
        data2.addColumn('string', 'yläkerta annotation');


        var a = [];
        var dt = [];
        for (var i = 0; i < 100; i++) {
//            alert(data.feeds[i].field1);
            if (data.feeds[i].field1) {
                a.push(parseFloat(data.feeds[i].field1));
                dt.push(data.feeds[i].created_at);
                
            }
        }

        for (var i = 0; i < dt.length; i++) {
            data2.addRow([new Date(dt[i]), a[i], undefined]);
        }
        /*
        data2.addRows([
            [new Date(dt[0]), a[0], "semmosta"],
            [new Date(dt[1]), a[1], "tommosta"],
            [new Date(dt[2]), a[2], "oho"]

        ]);
*/
        chart.draw(data2, {
            displayAnnotations: true,
        });


    });
}

google.load('visualization', '1.1', {
    'packages': ['annotationchart']
});
google.setOnLoadCallback(drawChart);
