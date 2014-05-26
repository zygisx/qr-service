'use strict';

var qrAppServices = angular.module('qrApp.Services', ['ngResource']);


qrAppServices.factory('Encode', function ($resource) {
    return $resource('/api/encode', {}, {
        image: {
            method: 'POST'
        }
    });
});

qrAppServices.factory('Decode', function ($resource) {
    return $resource('/api/decode', {}, {
        decode: {
            method: 'POST'
        }
    });
});



