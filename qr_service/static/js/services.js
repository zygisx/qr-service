'use strict';

var qrAppServices = angular.module('qrApp.Services', ['ngResource']);


qrAppServices.factory('Post', function($resource) {
		return $resource('/api/post/:postId', {}, {
			query: {
				method: 'GET',
				params: { postId: '' },
				isArray: true
			}
		});
	})
;



