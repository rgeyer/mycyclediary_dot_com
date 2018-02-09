/**
* AthleteComponentController
* @namespace mycyclediary.component.controllers
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.component.controllers')
    .controller('AthleteComponentController', AthleteComponentController);

  AthleteComponentController.$inject = ['$scope', '$mdDialog', 'Authentication', 'Component', 'Snackbar'];

  /**
  * @namespace AthleteComponentController
  */
  function AthleteComponentController($scope, $mdDialog, Authentication, Component, Snackbar) {
    var vm = this;

    vm.isAuthenticated = Authentication.isAuthenticated();
    vm.components = [];
    vm.filtered_components = [];
    vm.addDialOpen = false;
    vm.filterDialOpen = false;
    vm.searchBox = false;
    vm.filter = 'all';

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf mycyclediary.component.controllers.AthleteComponentController
    */
    function activate() {
      Component.all().then(componentsSuccessFn, componentsErrorFn);

      $scope.$on('component.created.submitted', function (event, component) {
        vm.components.push(component);
        vm.do_filter();
      });

      $scope.$on('component.created', function () {
        // TODO: Fetch the component and replace it in the collection.
      });

      $scope.$on('component.created.error', function () {
        vm.components.pop();
        vm.do_filter();
      });

      /**
      * @name componentsSuccessFn
      * @desc Update components array on view
      */
      function componentsSuccessFn(data, status, headers, config) {
        vm.components = data.data;
        vm.filtered_components = vm.components;
        angular.forEach(vm.components, function(value, key) {
          Component.aggregates(value.id, undefined, undefined).then(aggregateSuccessFn, aggregateErrorFn);

          function aggregateSuccessFn(data, status, headers, config) {
            value.meters_distance = data.data.meters_distance;
            value.meters_elevation = data.data.meters_elevation;
          }

          function aggregateErrorFn(data, status, headers, config) {
            // TODO: Probably just skip it?
          }
        });
      }

      /**
      * @name componentsErrorFn
      * @desc Show snackbar with error
      */
      function componentsErrorFn(data, status, headers, config) {
        Snackbar.error(data.error);
      }
    }

    /**
    * @name filter_bikes
    * @desc Filter components to only the bikes
    */
    vm.filter_bikes = function() {
      vm.clear_filter();
      vm.filter = 'bikes';
      vm.do_filter();
    }

    /**
    * @name filter_shoes
    * @desc Filter components to only the shoes
    */
    vm.filter_shoes = function() {
      vm.clear_filter();
      vm.filter = 'shoes'
      vm.do_filter();
    }

    /**
    * @name filter_compoments
    * @desc Filter components to only the components
    */
    vm.filter_components = function() {
      vm.clear_filter();
      vm.filter = 'components';
      vm.do_filter();
    }

    vm.do_filter = function() {
      vm.filtered_components = [];
      angular.forEach(vm.components, function(value, key) {
        if (vm.filter == 'components') {
          if (!value.isBike && !value.isShoe) {
            vm.filtered_components.push(value);
          }
        } else if (vm.filter == 'bikes') {
          if (value.isBike) {
            vm.filtered_components.push(value);
          }
        } else if (vm.filter == 'shoes') {
          if (value.isShoe) {
            vm.filtered_components.push(value);
          }
        } else {
          vm.filtered_components = vm.components;
        }
      });
    }

    /**
    * @name clear_filter
    * @desc Remove all filters, show everything again
    */
    vm.clear_filter = function() {
      vm.filter = 'all';
      $scope.searchText = '';
      vm.searchBox = false;
      vm.do_filter();
    }

    /**
    * @name search
    * @desc Search
    */
    vm.search = function() {
      vm.filtered_components = [];
      angular.forEach(vm.components, function(value, key) {
        if (value.name.toLowerCase().indexOf($scope.searchText.toLowerCase()) >= 0) {
          vm.filtered_components.push(value);
        }
      });
    }

    vm.new_bike = function($event) {
      return $mdDialog.show({
        targetEvent: $event,
        templateUrl: "/static/templates/component/new-component.html",
        controller: "NewComponentController",
        controllerAs: "vm",
        clickOutsideToClose: true,
        hasBackdrop: true,
        locals: {component_type: "bike"}
      });
    }

    vm.new_shoe = function($event) {
      return $mdDialog.show({
        targetEvent: $event,
        templateUrl: "/static/templates/component/new-component.html",
        controller: "NewComponentController",
        controllerAs: "vm",
        clickOutsideToClose: true,
        hasBackdrop: true,
        locals: {component_type: "shoe"}
      });
    }

    vm.new_component = function($event) {
      return $mdDialog.show({
        targetEvent: $event,
        templateUrl: "/static/templates/component/new-component.html",
        controller: "NewComponentController",
        controllerAs: "vm",
        clickOutsideToClose: true,
        hasBackdrop: true,
        locals: {component_type: "component"}
      });
    }
  }
})();
