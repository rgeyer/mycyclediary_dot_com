/**
* NavbarController
* @namespace mycyclediary.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.layout.controllers')
    .controller('NavbarController', NavbarController);

  NavbarController.$inject = ['$scope', 'Authentication', 'Snackbar'];

  /**
  * @namespace NavbarController
  */
  function NavbarController($scope, Authentication, Snackbar) {
    var vm = this;

    vm.logout = logout;

    /**
    * @name logout
    * @desc Log the user out
    * @memberOf mycyclediary.layout.controllers.NavbarController
    */
    function logout() {
      Authentication.logout().then(logoutSuccessFn, logoutErrorFn);

      /**
      * @name logoutSuccessFn
      * @desc Unauthenticate and redirect to index with page reload
      */
      function logoutSuccessFn(data, status, headers, config) {
        Authentication.unauthenticate();

        window.location = '/';
      }

      /**
      * @name logoutErrorFn
      * @desc Log "Epic failure!" to the console
      */
      function logoutErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.message);
      }
    }
  }
})();
