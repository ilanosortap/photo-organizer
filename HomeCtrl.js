angular.module('myApp', [])
    .controller("HomeCtrl", ['$scope', 'PostModel',
function($scope, PostModel) {

    $scope.Upload = function (element) {
        var data = new FormData();
        data.append('file', $(element)[0].files[0]);
        jQuery.ajax({
            url: 'http://127.0.0.1:5000/upload',
            type: 'post',
            data: data,
            contentType: false,
            processData: false,
            success: function (response) {
                console.log(response);
            },
            error: function (jqXHR, textStatus, errorMessage) {
                alert('Error uploading: ' + errorMessage);
            }
        });
    };
}])