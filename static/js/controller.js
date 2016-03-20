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

        var movie1 = $(this).find('input[name="movie1"]');

        $.getJSON('/structure', {movie1: movie1.val()})
        .done(function(data){
          alert(data);})
        .fail(function(jqxhr, textStatus, error){
          var err = textStatus + ", " + error;
          console.log("Request failed: " + err);
         });
        
    });

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


