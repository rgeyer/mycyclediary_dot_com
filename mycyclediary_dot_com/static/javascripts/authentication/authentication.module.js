(function () {
  'use strict';

  angular
    .module('mycyclediary.authentication', [
      'mycyclediary.authentication.controllers',
      'mycyclediary.authentication.services'
    ]);

  angular
    .module('mycyclediary.authentication.controllers', []);

  angular
    .module('mycyclediary.authentication.services', ['ngCookies']);
})();
