(function(){
	var app = angular.module('bootstrapDefinition', []);

	app.controller('bootstrapDefinitionController',
		['$http', function($http){
			var store = this;
			store.selector = [];
			$http.get('/bootstraplookup/bootstrapdeflookup').success(function(data){
				store.selector = data;
			});
		}]
	);

	app.directive('bootstrapDefinition', function(){
		return {
			restrict : 'E',
			templateUrl : "bootstrap-definition.html",
		};
	});

})();