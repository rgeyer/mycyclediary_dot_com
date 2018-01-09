(function () {
  'use strict';

  angular
    .module('mycyclediary.activities', [
      'mycyclediary.activities.controllers',
      'mycyclediary.activities.services'
    ]);

  angular
    .module('mycyclediary.activities.controllers', ['datatables', 'ngResource']);

  angular
    .module('mycyclediary.activities.services', []);
})();
