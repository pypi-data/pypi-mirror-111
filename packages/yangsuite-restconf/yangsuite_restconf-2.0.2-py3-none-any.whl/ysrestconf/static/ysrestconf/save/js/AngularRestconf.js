'use strict';

// Declare app level module which depends on views, and components
var app = angular.module('AngularRestconf', ['ngSanitize', 'ngRoute', 'swaggerUi', 'ui.bootstrap']);

app.controller('MainCtrl', function ($scope, $http, $sce, $location) {

	$scope.show_swagger_ui = false;
	$scope.show_api_button = false;
	$scope.show_more_button = false;
	$scope.show_clear_button = false;

	$scope.ClearSwagger = function() {
		$scope.show_swagger_status = false;
		$scope.show_swagger_ui = false;
		$scope.show_api_button = false;
		$scope.show_more_button = false;
		$scope.swagOverFlow = {};
	}

	function getHead(swagobj) {
		let swagHead = {}

		for (let key of Object.keys(swagobj)) {
			if (key != "paths") {
				swagHead[key] = swagobj[key];
			}
		}
		swagHead["paths"] = getNextGroup(swagobj["paths"], 50);
		return swagHead;
	}

	function getNextGroup(swagobj, count) {
		let paths = {};
		let keys = Object.keys(swagobj);

		if (keys && keys.length < count) {
			count = keys.length;
		}

		if (!keys || !keys.length > 0) {
			$scope.show_more_button = false;
			return;
		}

		for (let i = 0; i < count; i++) {
			paths[keys[i]] = swagobj[keys[i]];
			delete swagobj[keys[i]];
		}

		return paths;
	}

	$scope.ShowMoreAPIs = function() {
		$scope.show_swagger_ui = false;
		$scope.show_api_button = false;
		let pathNum = Object.keys($scope.swagOverFlow.paths).length;
		stopProgress($("#ys-progress"));
		if (pathNum == 0) {
			$scope.numPath = 0;
			$("#ys-progress").progressbar("destroy");
			$.jstree.destroy($("#tree"));
			$("#ys-warn-dialog")
	        .empty()
	        .dialog({
	            title: "All APIs Generated",
	            minHeight: 100,
	            maxWidth: 200,
	            buttons: {
	            	"Close": function () {
	            		$(this).dialog("close");
	            	},
	            }
	        })
	        .html('<pre>')
	        .append('All RESTCONF APIs have been shown.\n',
	        	    'If you wish to cycle through again,\n',
	        	    'click on "Load Module(s)". You may \n',
	        	    'want to choose a more specific branch \n',
	        	    'of the module tree next time.</pre>')
	        .dialog("open");
		}
	}

	$scope.LoadSchema = function() {
		if ($scope.swagOverFlow) {
			if ($scope.swagOverFlow.paths) {
				$scope.swagObj = {};
				$scope.show_swagger_ui = true;
				$scope.swagObj = getHead($scope.swagOverFlow);
				return;
			}
		}
		let csrf = Cookies.get('csrftoken');
		let yangset = $("#ytool-yangset").val();
		let device = $("#ytool-devices").val();
		let nodeIds = $("#tree").jstree(true).get_selected();
		let nodeData = [];
		$.each(nodeIds, function(i, n) {
			if (n != 1) {
			    let node = $("#tree").jstree(true).get_node(n);
			    nodeData.push(node.data);
			}
		});

		if (nodeData.length == 0) {
	        $("#ys-warn-dialog")
	        .empty()
	        .dialog({
	            title: "WARNING",
	            minHeight: 100,
	            maxWidth: 200,
	            buttons: {
	                "Continue": function () {
	                    $(this).dialog("close");
	                    let config = {
                            method: "GET",
					        url: $sce.trustAsResourceUrl('/restconf/genswag/'),
					        xsrfHeaderName: "X-CSRFToken",
					        xsrfCookieName: csrf,
				            headers: {
				            	'Content-type': 'application/json',
				            	"X-CSRFToken": csrf,
				            },
				            params: {"models": $scope.models,
				                     "yangset": yangset,
				                     "device": device,
				                     "nodes": nodeData}
					    }
					    startProgress($("#ys-progress"),
					    	          '/restconf/genstatus/');
						$http(config).then(function(retObj) {
							$scope.swagOverFlow = retObj.data.swagobj;
							$scope.show_swagger_ui = true;
							$scope.swagObj = getHead($scope.swagOverFlow);
							$scope.show_more_button = true;
							stopProgress($("#ys-progress"));
							
						}, function(retObj) {
							stopProgress($("#ys-progress"));
						});
	            	},
	            	"Cancel": function () {
	            		$(this).dialog("close");
	            		return;
	            	},
	            }
	        })
	        .html('<pre>')
	        .append('If this is a large module it could take\n',
	        	    'several minutes to generate the APIs.\n',
	        	    'You may want to consider choosing a branch\n',
	        	    'of the module and only generate those APIs.</pre>')
	        .dialog("open");
		} else {
			let config = {
				method: "GET",
		        url: $sce.trustAsResourceUrl('/restconf/genswag/'),
		        xsrfHeaderName: "X-CSRFToken",
		        xsrfCookieName: csrf,
	            headers: {
	            	'Content-type': 'application/json',
	            	"X-CSRFToken": csrf,
	            },
	            params: {"models": $scope.models,
	                     "yangset": yangset,
	                     "device": device,
	                     "nodes": nodeData}
		    }
		    startProgress($("#ys-progress"),
		    	          '/restconf/genstatus');
			$http(config).then(function(retObj) {
				$scope.swagOverFlow = retObj.data.swagobj;
				$scope.show_swagger_ui = true;
				$scope.swagObj = getHead($scope.swagOverFlow);
				$scope.show_more_button = true;
				stopProgress($("#ys-progress"));
				
			}, function(retObj) {
				stopProgress($("#ys-progress"));
			});
		}
	}
});
