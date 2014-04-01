'use strict';

var qrAppServices = angular.module('qrApp.Services', ['ngResource']);


qrAppServices.factory('Encode', function ($resource) {
    return $resource('/api/encode', {}, {
        image: {
            method: 'get',
            headers: {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
        }
    });
})
;



