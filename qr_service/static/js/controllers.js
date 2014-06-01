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
            if (day<10){
                day="0" + day;
            }
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
                date: $scope.signDate,
                purchaseDate:  $scope.purchaseDate,
                invoiceSerie:  $scope.invoiceSerie,
                invoiceNumber: $scope.invoiceNumber,
                providerId: $scope.providerId,
                receiverId: $scope.receiverId,
                items: $scope.items
            });

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

qrAppControllers.controller('DecodeCtrl', ['$scope', 'Decode', '$upload',
    function($scope, Decode, $upload) {
        function renderResult(data) {
            console.log(data);
            $scope.signDate = data.date;
            $scope.purchaseDate = data.purchaseDate;
            $scope.invoiceSerie = data.invoiceSerie;
            $scope.invoiceNumber = data.invoiceNumber;
            $scope.providerId = data.providerId;
            $scope.receiverId = data.receiverId;

            $scope.items = [];
            data.items.forEach(function(item) {
                $scope.items.push({
                    id: item.id,
                    units: item.units,
                    unitPrice: item.unitPrice,
                    taxableValue: item.taxableValue,
                    vat: item.vat,
                    vatAmount: item.vatAmount
                })
            })

            $scope.showData = true;
        }

        $scope.data = "";
        $scope.showData = false;

        $scope.onUpload = function($file) {
        //$files: an array of files selected, each file has name, size, and type.

          $scope.upload = $upload.upload({
            url: 'api/decodeImage',
            file: $file
          }).success(function(data, status, headers, config) {
            // file is uploaded successfully
            console.log(data);
            renderResult(data);
          }).error(function(error) {
                $scope.errorMessage = "Klaida dekoduojant sąskaitą faktūrą.";
          });
        };

       $scope.submit = function() {
            var decode = new Decode({
                data: $scope.data
            });
            decode.$decode(function(resp) {
                console.log(resp)
                renderResult(resp)

            }, function(error) {
                $scope.errorMessage = "Klaida dekoduojant sąskaitą faktūrą.";
            });


       };

    }
]);
