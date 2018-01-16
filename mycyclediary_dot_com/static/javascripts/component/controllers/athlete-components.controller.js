/**
* AthleteComponentController
* @namespace mycyclediary.component.controllers
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.component.controllers')
    .controller('AthleteComponentController', AthleteComponentController);

  AthleteComponentController.$inject = ['$scope', 'Authentication', 'Component', 'Snackbar'];

  /**
  * @namespace AthleteComponentController
  */
  function AthleteComponentController($scope, Authentication, Component, Snackbar) {
    var vm = this;

    vm.isAuthenticated = Authentication.isAuthenticated();
    vm.components = [];

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf mycyclediary.component.controllers.AthleteComponentController
    */
    function activate() {
      Component.components().then(componentsSuccessFn, componentsErrorFn);

      $scope.$on('component.created', function (event, component) {
        vm.components.unshift(component);
      });

      $scope.$on('component.created.error', function () {
        vm.components.shift();
      });

      /**
      * @name componentsSuccessFn
      * @desc Update components array on view
      */
      function componentsSuccessFn(data, status, headers, config) {
        vm.components = data.data;
      }

      /**
      * @name componentsErrorFn
      * @desc Show snackbar with error
      */
      function componentsErrorFn(data, status, headers, config) {
        Snackbar.error(data.error);
      }
    }
  }
})();
