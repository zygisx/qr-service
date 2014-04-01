'use strict';

/* Controllers */

var qrAppControllers = angular.module('qrApp.Controllers', []);

qrAppControllers.controller('IndexCtrl', ['$scope',
    function($scope) {
    }
]);

qrAppControllers.controller('FormCtrl', ['$scope', 'Encode',
    function($scope) {

        $scope.submitedData = "";

        $scope.submit = function() {
            $scope.submitedData = $scope.data;
        }
    }
]);
