'use strict';

/* Controllers */

var qrAppControllers = angular.module('qrApp.Controllers', []);

qrAppControllers.controller('IndexCtrl', ['$scope',
    function($scope) {
    }
]);

qrAppControllers.controller('FormCtrl', ['$scope', 'Encode',
    function($scope, Encode) {
        function todaysDate() {
            var d = new Date();
            var year = d.getFullYear();
            var month = d.getMonth()+1;
            if (month<10){
                month="0" + month;
            };
            var day = d.getDate();
            return year + "-" + month + "-" + day;
        }

        $scope.qrImage = "";

        $scope.items = [{id: "", units:"", unitPrice: "", taxableValue: "", vat: "", vatAmount: ""}];
        $scope.errorCorrection = "M";
        $scope.errorMessage = "";

        $scope.signDate = todaysDate();
        $scope.purchaseDate = todaysDate();

        $scope.submit = function() {

            var encode = new Encode({
                data: $scope.data,
                date: $scope.signDate,
                purchaseDate:  $scope.purchaseDate,
                invoiceSerie:  $scope.invoiceSerie,
                invoiceNumber: $scope.invoiceNumber,
                providerId: $scope.providerId,
                receiverId: $scope.receiverId,
                items: $scope.items
            });
            console.log($scope.items)

            encode.$image(function(resp) {
                $scope.qrImage = resp.image;
                console.log(resp.msg)
                $scope.errorMessage = "";
            
            }, function(error) {
                $scope.errorMessage = "Klaida koduojant sąskaitą faktūrą.";
            });
        }

        $scope.addItem = function() {
            $scope.items.push(
                {id: "", units:"", unitPrice: "", taxableValue: "", vat: "", vatAmount: ""}
            )
        }
        $scope.removeItem = function(index) {
            $scope.items.splice(index, 1);
        };

    }
]);
