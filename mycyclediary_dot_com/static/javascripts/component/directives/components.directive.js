/**
* Component
* @namespace mycyclediary.component.directives
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.component.directives')
    .directive('components', components);

  /**
  * @namespace Component
  */
  function components() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf mycyclediary.component.directives.Component
    */
    var directive = {
      controller: 'ComponentController',
      controllerAs: 'vm',
      restrict: 'E',
      scope: {
        components: '='
      },
      templateUrl: '/static/templates/component/components.html'
    };

    return directive;
  }
})();
