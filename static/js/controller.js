var app_graph = angular.module('myAppGraph', []);
app_graph.controller('formController', function($scope) {
    $scope.firstName = "Rodrigo";
    $scope.visible = null;
    $scope.alignment = null;


    angular.element(document).ready(function () {

        $("#form_content").hide();
        $("#form_structure").hide();
        //$("#intro").css("background-color", "yellow");
        $("#structure_metrics_button").click(function(){
            $("#form_structure").show();
            $("#form_content").hide();
        });
        $("#content_metrics_button").click(function(){
            $("#form_structure").hide();
            $("#form_content").show();
        });

    });

    $('#structure_form').on('submit', function(e){
        e.preventDefault();
        var select = "none"
        select = $(this).find('#select_metric').val();
        var movie1 = $(this).find('#first_movie option:selected').text();
        console.log(movie1);
        var movie2 = $(this).find('#second_movie option:selected').text();
        console.log(movie2);
        var lengthvar = "2";
        // var movie1 = $(this).find('input[name="movie1"]');
        // var movie2 = $(this).find('input[name="movie2"]');

        if(select === "distance"){
          $.getJSON('/temporal_distance', {movie1: movie1, movie2: movie2})
          .done(function(data){
            parseDistance(data);
            })
          .fail(function(jqxhr, textStatus, error){
          var err = textStatus + ", " + error;
          console.log("Request failed: " + err);
         });
        }else if (select === "centrality"){
          $.getJSON('/centrality', {movie1: movie1, movie2: movie2})
          .done(function(data){
            parseCentrality(data);})
          .fail(function(jqxhr, textStatus, error){
          var err = textStatus + ", " + error;
          console.log("Request failed: " + err);
         });
        }else if (select === "reachability"){
          $.getJSON('/reachability', {movie1: movie1, movie2: movie2})
          .done(function(data){
            parseReachability(data);
            })
          .fail(function(jqxhr, textStatus, error){
          var err = textStatus + ", " + error;
          console.log("Request failed: " + err);
         });
        } else {
          alert("none filled in")
        }
        
    });

    function parseCentrality(data) {
      var total = 0;
      
      for(var d = 0; d < data.length; d++) {
        dataset = data[d]
        var result = [];
        for(var i = 0; i < dataset.length; i++) {
          total = total + dataset[i][1]
          date = new Date(dataset[i][0]*1000);
          result.push([date, total]);
        }
        console.log(result);
        graphLine(result, "#graph" + (d+1));
      }
      
    }

    function parseReachability(dataset) {
      result = [];
       
      var min = [/*[2, 1460584800],*/[4, 1460584800],[6, 1460584800],[8, 1460584800]];
      for(var r = 0; r < dataset.length; r++) {
        record = dataset[r]
        query = Math.floor(r/200); 
        var max = 0;
        for(var t = 1; t < record.length; t++) {
          if (record[t] > max) {
            max = record[t]
          }
        }
        
        if(max < min[query][1]) {
          for(var i = query; i < min.length; i++){
            console.log("Record: " + r + "Minima: " + min)
            min[i][1] = max

          }
          
        } 
      }

      for(var m = 0; m < min.length; m++) {
        date = new Date(min[m][1]*1000);
        day = new Date(date.setHours(0,0,0,0));
        result.push([min[m][0], day]);
      }     

      graphLine(result, "#graph1");
    }

    function parseDistance(dataset) {
      result = [];
      for(var i = 0; i < dataset.length; i++) {
        entry = dataset[i]
        var max = 0;
        for(var j = 0; j < entry.length; j++) {
          if(entry[j] > max){
            max = entry[j]
          }
        }
        date = new Date(max*1000);
        day = new Date(date.setHours(0,0,0,0));
        result.push([day, Math.floor(Math.random()*2)]);
      }
      result.sort(function(x,y) {
        return x[0] - y[0]
      })
      console.log(result[0]);
      graphLine(result);
    }

    function graphLine(data, selector) {//Works with 2d array
      // Set the dimensions of the canvas / graph
      var margin = {top: 50, right: 20, bottom: 30, left: 150},
          width = 600 - margin.left - margin.right,
          height = 450 - margin.top - margin.bottom;

      // Parse the date / time
      var parseDate = d3.time.format("%d-%b-%y").parse;

      // Set the ranges
      var x = d3.time.scale().range([0, width]);
      var y = d3.scale.linear().range([height, 0]);

      // Define the axes
      var xAxis = d3.svg.axis().scale(x)
          .orient("bottom").ticks(4);

      var yAxis = d3.svg.axis().scale(y)
          .orient("left").ticks(5);

      // Define the line
      var valueline = d3.svg.line()
          .x(function(d) { return x(d[0]); })
          .y(function(d) { return y(d[1]); });
          
      // Adds the svg canvas
      var svg = d3.select(selector)
          .append("svg")
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
          .append("g")
              .attr("transform", 
                    "translate(" + margin.left + "," + margin.top + ")");

          // Scale the range of the data
      x.domain(d3.extent(data, function(d) { return d[0]; }));
      y.domain([0, d3.max(data, function(d) { return d[1]; })]);

      // Add the valueline path.
      svg.append("path")
          .attr("class", "line")
          .attr("d", valueline(data));

      // Add the X Axis
      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

      // Add the Y Axis
      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis);
    }

    $('#content_form').on('submit', function(e){
        e.preventDefault();

        var movie1 = $(this).find('input[name="movie1_rating"]');

        $.getJSON('/content', {movie1_rating: movie1.val()})
        .done(function(data){
          alert(data);})
        .fail(function(jqxhr, textStatus, error){
          var err = textStatus + ", " + error;
          console.log("Request failed: " + err);
         });
        
    });


});

var app = angular.module("MyApp", []);

app.controller("PostsCtrl", function($scope, $http) {
  $http.get('http://rest-service.guides.spring.io/greeting',{ //starting http get example
      params: {
      }
  }).
    success(function(data, status, headers, config) {
      $scope.posts = data;

    }).
    error(function(data, status, headers, config) {
      // log error
    });

    var settings = {
      "async": true,
      "crossDomain": true,
      "url": "http://localhost:7474/db/data/cypher",
      "method": "POST",
      "headers": {
        "authorization": "Basic bmVvNGo6Um9kcm8xMjM9",
        "cache-control": "no-cache"
      },
      "data": "{\r\n  \"query\" : \"MATCH (n: Person) return n\",\r\n  \"params\" : {\r\n  }\r\n}"
    };
    $http(settings). // example to request post form neo4j
    success(function(data, status, headers, config) {
      //console.log(JSON.stringify(data));
        console.log(data);
    }).
    error(function(data, status, headers, config) {
      // log error
    });

    var query = 'MATCH (n) return n';
    var sett2 = {
      "async": true,
      "crossDomain": true,
      "url": "http://localhost:7474/db/data/transaction/commit",
      "method": "POST",
      "headers": {
        "authorization": "Basic bmVvNGo6Um9kcm8xMjM9",
        "content-type": "application/json",
        "cache-control": "no-cache",
        "postman-token": "3c44f77a-bd69-b466-cfeb-41cd047cd5c7"
      },
      "processData": false,
      "data": "{\r\n  \"statements\" : [ {\r\n    \"statement\" : \""+query+"\",\r\n    \"resultDataContents\" : [ \"row\", \"graph\" ]\r\n  } ]\r\n}"
    };
    $http(sett2).
    success(function(data, status, headers, config) {
      console.log(JSON.stringify(data));
       // console.log(data);
    }).
    error(function(data, status, headers, config) {
      // log error
    });



});


/*post with jquery
var settings = {
  "async": true,
  "crossDomain": true,
  "url": "http://localhost:7474/db/data/cypher",
  "method": "POST",
  "headers": {
    "authorization": "Basic bmVvNGo6Um9kcm8xMjM9",
    "cache-control": "no-cache",
    "postman-token": "790f0b8e-dab6-8d66-d064-a1111fd0cee2"
  },
  "data": "{\r\n  \"query\" : \"MATCH (n: Person) return n\",\r\n  \"params\" : {\r\n  }\r\n}"
};

$.ajax(settings).done(function (response) {
  console.log(response);
});
* */


