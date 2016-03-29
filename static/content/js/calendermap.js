//https://formden.com/blog/date-picker
//http://eternicode.github.io/bootstrap-datepicker/?markup=input&format=&weekStart=&startDate=&endDate=&startView=0&minViewMode=0&maxViewMode=2&todayBtn=false&clearBtn=false&language=en&orientation=auto&multidate=&multidateSeparator=&keyboardNavigation=on&forceParse=on#sandbox
//http://www.unixtimestamp.com/index.php
$(function() {

    var start_date_input=$('input[name="start_date"]'); //our date input has the name "date"
    var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
    start_date_input.datepicker({
        format: 'dd-mm-yyyy',
        container: container,
        todayHighlight: true,
        autoclose: true,
        startDate: "01/01/1996",
        endDate: "31/12/2016"
    });
    var end_date_input=$('input[name="end_date"]'); //our date input has the name "date"
    var container2=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
    end_date_input.datepicker({
        format: 'dd-mm-yyyy',
        container: container2,
        todayHighlight: true,
        autoclose: true,
        startDate: "01/01/1996",
        endDate: "31/12/2016"
    });

    $('#update_chart').click(function() {
        var movie_title_form = $('#movie_title').val(); //Toy Story (1995)

        var start_date_split = start_date_input.val().split("-");
        var start_date_form = start_date_split[2]+start_date_split[1]+start_date_split[0];

        //console.log(start_date_form);
        //parseInt(start_date_split[2]), parseInt(end_date_split[2])
        //console.log('Year of start date is: ' + parseInt(start_date_split[2]));
        var end_date_split = end_date_input.val().split("-");
        var end_date_form = end_date_split[2]+end_date_split[1]+end_date_split[0];

        var year_start = parseInt(start_date_split[2]);
        var year_end = parseInt(end_date_split[2]) + 1;
        //console.log('Year start: ' + year_start + 'Year end: ' + year_end);
        //var end_date_form = $('#end_date').val();

        console.log('movie title has: ' + movie_title_form);
        console.log('start date has: ' + start_date_form);
        console.log('end date has: ' + end_date_form);




        $('div.calender-map').empty(); //remove first everything

        var url_service = 'http://127.0.0.1:5000/timestamps_ratings?movie_title='+ movie_title_form+'' +
                                '&date_from='+ start_date_form+'' +
                                '&date_to='+end_date_form+'';
        //console.log(url_service);
        var url_service_encoded = encodeURI(url_service);

        var width = 900,
            height = 105,
            cellSize = 12; // cell size
            week_days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
            month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

        var day = d3.time.format("%w"),
            week = d3.time.format("%U"),
            percent = d3.format(".1%"),
            format = d3.time.format("%Y%m%d");
            parseDate = d3.time.format("%Y%m%d").parse;

        var color = d3.scale.linear().range(["white", '#002b53'])
            .domain([0, 1])

        var svg = d3.select(".calender-map").selectAll("svg")
            .data(d3.range(year_start, year_end))
          .enter().append("svg")
            .attr("width", '100%')
            .attr("data-height", '0.5678')
            .attr("viewBox",'0 0 900 105')
            .attr("class", "RdYlGn")
          .append("g")
            .attr("transform", "translate(" + ((width - cellSize * 53) / 2) + "," + (height - cellSize * 7 - 1) + ")");

        svg.append("text")
            .attr("transform", "translate(-38," + cellSize * 3.5 + ")rotate(-90)")
            .style("text-anchor", "middle")
            .text(function(d) { return d; });

        for (var i=0; i<7; i++)
        {
        svg.append("text")
            .attr("transform", "translate(-5," + cellSize*(i+1) + ")")
            .style("text-anchor", "end")
            .attr("dy", "-.25em")
            .text(function(d) { return week_days[i]; });
         }

        var rect = svg.selectAll(".day")
            .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
          .enter()
            .append("rect")
            .attr("class", "day")
            .attr("width", cellSize)
            .attr("height", cellSize)
            .attr("x", function(d) { return week(d) * cellSize; })
            .attr("y", function(d) { return day(d) * cellSize; })
            .attr("fill",'#fff')
            .datum(format);

        var legend = svg.selectAll(".legend")
              .data(month)
            .enter().append("g")
              .attr("class", "legend")
              .attr("transform", function(d, i) { return "translate(" + (((i+1) * 50)+8) + ",0)"; });

        legend.append("text")
           .attr("class", function(d,i){ return month[i] })
           .style("text-anchor", "end")
           .attr("dy", "-.25em")
           .text(function(d,i){ return month[i] });

        svg.selectAll(".month")
            .data(function(d) { return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
          .enter().append("path")
            .attr("class", "month")
            .attr("id", function(d,i){ return month[i] })
            .attr("d", monthPath);




        d3.json(url_service_encoded, function(error, data) {
            //load values
            var my_dates = data.Date;
            var my_values = data.Comparison_Value;
            //get max
            var arr = Object.keys( my_values ).map(function ( key ) { return my_values[key]; });
            var max = Math.max.apply( null, arr );
            //console.log(max);
            //size
            var size_data = Object.keys(my_dates).length;
            var results = {};

            for (i = 0; i < size_data; i++) {
                results[my_dates[i]] = Math.sqrt(my_values[i] / max);
                //results[my_dates[i]] = my_values[i] / max;
                //console.log(Math.sqrt(my_values[i] / max));
                if(my_values[i] / max == 1){
                    console.log('Max day is: ' + my_dates[i] + 'with value of: ' + my_values[i]);
                }
            }
            //console.log(results);

            rect.filter(function(d) { return d in results; })
              .attr("fill", function(d) { return color(results[d]); })
              .attr("data-title", function(d) { return "value : "+Math.round(results[d]*100)});
            $("rect").tooltip({container: 'body', html: true, placement:'top'});


        });

        function numberWithCommas(x) {
            x = x.toString();
            var pattern = /(-?\d+)(\d{3})/;
            while (pattern.test(x))
                x = x.replace(pattern, "$1,$2");
            return x;
        }

        function monthPath(t0) {
          var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
              d0 = +day(t0), w0 = +week(t0),
              d1 = +day(t1), w1 = +week(t1);
          return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
              + "H" + w0 * cellSize + "V" + 7 * cellSize
              + "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
              + "H" + (w1 + 1) * cellSize + "V" + 0
              + "H" + (w0 + 1) * cellSize + "Z";
        }


    });
});


//var width = 900,
//    height = 105,
//    cellSize = 12; // cell size
//    week_days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
//    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
//
//var day = d3.time.format("%w"),
//    week = d3.time.format("%U"),
//    percent = d3.format(".1%"),
//	format = d3.time.format("%Y%m%d");
//	parseDate = d3.time.format("%Y%m%d").parse;
//
//var color = d3.scale.linear().range(["white", '#002b53'])
//    .domain([0, 1])
//
//var svg = d3.select(".calender-map").selectAll("svg")
//    .data(d3.range(1996, 2017))
//  .enter().append("svg")
//    .attr("width", '100%')
//    .attr("data-height", '0.5678')
//    .attr("viewBox",'0 0 900 105')
//    .attr("class", "RdYlGn")
//  .append("g")
//    .attr("transform", "translate(" + ((width - cellSize * 53) / 2) + "," + (height - cellSize * 7 - 1) + ")");
//
//svg.append("text")
//    .attr("transform", "translate(-38," + cellSize * 3.5 + ")rotate(-90)")
//    .style("text-anchor", "middle")
//    .text(function(d) { return d; });
//
//for (var i=0; i<7; i++)
//{
//svg.append("text")
//    .attr("transform", "translate(-5," + cellSize*(i+1) + ")")
//    .style("text-anchor", "end")
//    .attr("dy", "-.25em")
//    .text(function(d) { return week_days[i]; });
// }
//
//var rect = svg.selectAll(".day")
//    .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
//  .enter()
//	.append("rect")
//    .attr("class", "day")
//    .attr("width", cellSize)
//    .attr("height", cellSize)
//    .attr("x", function(d) { return week(d) * cellSize; })
//    .attr("y", function(d) { return day(d) * cellSize; })
//    .attr("fill",'#fff')
//    .datum(format);
//
//var legend = svg.selectAll(".legend")
//      .data(month)
//    .enter().append("g")
//      .attr("class", "legend")
//      .attr("transform", function(d, i) { return "translate(" + (((i+1) * 50)+8) + ",0)"; });
//
//legend.append("text")
//   .attr("class", function(d,i){ return month[i] })
//   .style("text-anchor", "end")
//   .attr("dy", "-.25em")
//   .text(function(d,i){ return month[i] });
//
//svg.selectAll(".month")
//    .data(function(d) { return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
//  .enter().append("path")
//    .attr("class", "month")
//    .attr("id", function(d,i){ return month[i] })
//    .attr("d", monthPath);
//
//
//var url_service = "http://127.0.0.1:5000/timestamps_ratings";
//var url_service_encoded = encodeURI(url_service);
//
//var url_service2 = 'http://127.0.0.1:5000/timestamps_ratings?movie_title=Toy Story (1995)&date_from=19960129&date_to=19961229';
//var url_service_encoded2 = encodeURI(url_service2);
//d3.json(url_service_encoded2, function(error, data) {
//    //load values
//    var my_dates = data.Date;
//    var my_values = data.Comparison_Value;
//    //get max
//    var arr = Object.keys( my_values ).map(function ( key ) { return my_values[key]; });
//    var max = Math.max.apply( null, arr );
//    //console.log(max);
//    //size
//    var size_data = Object.keys(my_dates).length;
//    var results = {};
//
//    for (i = 0; i < size_data; i++) {
//        results[my_dates[i]] = Math.sqrt(my_values[i] / max);
//        //console.log(Math.sqrt(my_values[i] / max));
//        if(my_values[i] / max == 1){
//            console.log('Hay max el dia: ' + my_dates[i] + 'con el valor de: ' + my_values[i]);
//        }
//    }
//    //console.log(results);
//
//    rect.filter(function(d) { return d in results; })
//      .attr("fill", function(d) { return color(results[d]); })
//	  .attr("data-title", function(d) { return "value : "+Math.round(results[d]*100)});
//	$("rect").tooltip({container: 'body', html: true, placement:'top'});
//
//
//});
//
////d3.csv("data.csv", function(error, csv) {
////  csv.forEach(function(d) {
////    d.Comparison_Type = parseInt(d.Comparison_Type);
////      //console.log(d.Comparison_Type)
////  });
////
//// var Comparison_Type_Max = d3.max(csv, function(d) { return d.Comparison_Type; });
////  var data = d3.nest()
////    .key(function(d) { return d.Date; })
////    .rollup(function(d) { return  Math.sqrt(d[0].Comparison_Type / Comparison_Type_Max); })
////    .map(csv);
////
////  console.log(data);
////
////  rect.filter(function(d) { return d in data; })
////      .attr("fill", function(d) { return color(data[d]); })
////	  .attr("data-title", function(d) { return "value : "+Math.round(data[d]*100)});
////	$("rect").tooltip({container: 'body', html: true, placement:'top'});
////});
//
//function numberWithCommas(x) {
//    x = x.toString();
//    var pattern = /(-?\d+)(\d{3})/;
//    while (pattern.test(x))
//        x = x.replace(pattern, "$1,$2");
//    return x;
//}
//
//function monthPath(t0) {
//  var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
//      d0 = +day(t0), w0 = +week(t0),
//      d1 = +day(t1), w1 = +week(t1);
//  return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
//      + "H" + w0 * cellSize + "V" + 7 * cellSize
//      + "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
//      + "H" + (w1 + 1) * cellSize + "V" + 0
//      + "H" + (w0 + 1) * cellSize + "Z";
//}
