/**
* Register controller
* @namespace mycyclediary.authentication.controllers
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.authentication.controllers')
    .controller('RegisterController', RegisterController);

  RegisterController.$inject = ['$location', '$scope', 'Authentication', 'Snackbar'];

  /**
  * @namespace RegisterController
  */
  function RegisterController($location, $scope, Authentication, Snackbar) {
    var vm = this;

    vm.register = register;

    activate();

    /**
     * @name activate
     * @desc Actions to be performed when this controller is instantiated
     * @memberOf thinkster.authentication.controllers.RegisterController
     */
    function activate() {
      // If the user is authenticated, they should not be here.
      if (Authentication.isAuthenticated()) {
        $location.url('/');
      }
    }

    /**
    * @name register
    * @desc Register a new user
    * @memberOf mycyclediary.authentication.controllers.RegisterController
    */
    function register() {
      if(!vm.email || !vm.password) { return; }
      Authentication.register(vm.email, vm.password)
        .then(registerSuccessFn, registerErrorFn);

      /**
       * @name registerSuccessFn
       * @desc Unauthenticate and redirect to index with page reload
       */
      function registerSuccessFn(data, status, headers, config) {
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

      /**
       * @name registerErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function registerErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.message);
      }
    }
  }
})();
