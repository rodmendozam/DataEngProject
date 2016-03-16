
var app_graph = angular.module('myAppGraph', []);
app_graph.controller('myCtrl', function($scope) {
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


});
