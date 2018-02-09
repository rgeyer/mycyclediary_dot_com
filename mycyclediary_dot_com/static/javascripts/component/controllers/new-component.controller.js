/**
* NewComponentController
* @namespace mycyclediary.component.controllers
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.component.controllers')
    .controller('NewComponentController', NewComponentController);

  NewComponentController.$inject = ['$rootScope', '$scope', '$mdDialog', 'component_type', 'Component', 'Snackbar'];

  /**
  * @namespace NewComponentController
  */
  function NewComponentController($rootScope, $scope, $mdDialog, component_type, Component, Snackbar) {
    var vm = this;

    vm.component_type = component_type;
    vm.name = undefined;
    vm.description = undefined;
    vm.brand_name = undefined;
    vm.model_name = undefined;
    vm.aquisition_date = undefined;
    vm.aquisition_distance_meters = undefined;
    vm.battery = false;
    vm.battery_rechargable = false;

    /**
    * @name submit
    * @desc Submit the form to create a new component
    * @memberOf mycyclediary.component.controllers.NewComponentController
    */
    vm.submit = function() {
      var new_component = {
        name: vm.name,
        description: vm.description,
        brand_name: vm.brand_name,
        model_name: vm.model_name
      }
      if (vm.component_type == 'bike') {
        new_component['isBike'] = true;
      }
      if (vm.component_type == 'shoe') {
        new_component['isShoe'] = true;
      }
      $rootScope.$broadcast('component.created.submitted', new_component);
      $mdDialog.hide();

      var battery = 1;
      if (vm.battery) {
        battery = 3;
        if (vm.battery_rechargable) {
          battery = 2;
        }
      }
      Component.create(vm.component_type, vm.name, vm.description, vm.brand_name, vm.model_name, undefined, vm.aquisition_date, vm.aquisition_distance_meters, undefined, battery)
        .then(createComponentSuccessFn, createComponentErrorFn);

      function createComponentSuccessFn(data, status, headers, config) {
        $rootScope.$broadcast('component.created');
        Snackbar.show('Success! Component created.');
      }

      function createComponentErrorFn(data, status, headers, config) {
        $rootScope.$broadcast('component.created.error');
        Snackbar.error(data.error);
      }
    }
  }
})();
