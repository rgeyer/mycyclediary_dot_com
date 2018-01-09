/**
* LoginController
* @namespace mycyclediary.authentication.controllers
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.authentication.controllers')
    .controller('LoginController', LoginController);

  LoginController.$inject = ['$location', '$scope', 'Authentication', 'Snackbar'];

  /**
  * @namespace LoginController
  */
  function LoginController($location, $scope, Authentication, Snackbar) {
    var vm = this;

    vm.login = login;

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf mycyclediary.authentication.controllers.LoginController
    */
    function activate() {
      // If the user is authenticated, they should not be here.
      if (Authentication.isAuthenticated()) {
        $location.url('/');
      }
    }

    /**
    * @name login
    * @desc Log the user in
    * @memberOf mycyclediary.authentication.controllers.LoginController
    */
    function login() {
      Authentication.login(vm.email, vm.password)
        .then(loginSuccessFn, loginErrorFn);

      /**
       * @name loginSuccessFn
       * @desc Unauthenticate and redirect to index with page reload
       */
      function loginSuccessFn(data, status, headers, config) {
        Authentication.setAuthenticatedAccount(data.data);

        window.location = '/';
      }

      /**
       * @name loginErrorFn
       * @desc Create a snackbar error
       */
      function loginErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.message);
      }
    }
  }
})();
