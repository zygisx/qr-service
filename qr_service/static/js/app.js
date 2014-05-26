'use strict';

var qrApp = angular.module('qrApp',[
        'ngRoute',
        'ngResource',
        'qrApp.Services',
        'qrApp.Controllers',
        'angularFileUpload'
    ]);


qrApp.config(['$routeProvider', '$locationProvider',
        function ($routeProvider, $locationProvider) {
            $routeProvider
                .when('/', {
                    templateUrl: 'static/partials/main.html',
                    controller: 'IndexCtrl'
                })
                .when('/form', {
                    templateUrl: 'static/partials/form.html',
                    controller: 'FormCtrl'
                })
                .when('/decode', {
                    templateUrl: 'static/partials/decode.html',
                    controller: 'DecodeCtrl'
                })
                .when('/description', {
                    templateUrl: 'static/partials/main.html',
                    controller: 'IndexCtrl'
                })
                .otherwise({
                    redirectTo: '/'
                })
            ;

            $locationProvider.html5Mode(true);
        }]);