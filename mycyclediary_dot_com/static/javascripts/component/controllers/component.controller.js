/**
* ComponentController
* @namespace mycyclediary.component.controllers
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.component.controllers')
    .controller('ComponentController', ComponentController);

  ComponentController.$inject = ['$scope'];

  /**
  * @namespace ComponentController
  */
  function ComponentController($scope) {
    var vm = this;

    vm.components = [];

    activate();


    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf mycyclediary.component.controllers.ComponentController
    */
    function activate() {
      $scope.$watchCollection(function () { return $scope.components; }, render);
    }


    /**
    * @name render
    * @desc Renders Components
    * @param {Array} current The current value of `vm.components`
    * @param {Array} original The value of `vm.components` before it was updated
    * @memberOf mycyclediary.component.controllers.ComponentController
    */
    function render(current, original) {
      if (current !== original) {
        vm.components = current;
      }
    }
  }
})();
