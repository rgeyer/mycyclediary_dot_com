/**
* Component
* @namespace mycyclediary.components.directives
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.component.directives')
    .directive('component', component);

  /**
  * @namespace Component
  */
  function component() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf mycyclediary.component.directives.Component
    */
    var directive = {
      restrict: 'E',
      scope: {
        component: '='
      },
      templateUrl: '/static/templates/component/component.html'
    };

    return directive;
  }
})();
