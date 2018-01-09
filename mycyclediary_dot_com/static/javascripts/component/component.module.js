(function () {
  'use strict';

  angular
    .module('mycyclediary.component', [
      'mycyclediary.component.controllers',
      'mycyclediary.component.directives',
      'mycyclediary.component.services'
    ]);

  angular
    .module('mycyclediary.component.controllers', []);

  angular
    .module('mycyclediary.component.directives', ['ngDialog']);

  angular
    .module('mycyclediary.component.services', []);
})();
