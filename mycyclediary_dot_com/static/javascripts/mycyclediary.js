(function () {
  'use strict';

  angular
    .module('mycyclediary', [
      'mycyclediary.config',
      'mycyclediary.routes',
      'mycyclediary.authentication',
      'mycyclediary.layout',
      'mycyclediary.utils',
      'mycyclediary.profiles',
      'mycyclediary.activities',
      'mycyclediary.component'
    ]);

  angular
    .module('mycyclediary.routes', ['ngRoute']);

  angular
    .module('mycyclediary.config', []);

  angular
    .module('mycyclediary')
    .run(run);

  run.$inject = ['$http'];

  /**
  * @name run
  * @desc Update xsrf $http headers to align with Django's defaults
  */
  function run($http) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
  }
})();
