/**
* StravaAuthCallbackController
* @namespace mycyclediary.strava.controllers
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.strava.controllers')
    .controller('StravaAuthCallbackController', StravaAuthCallbackController);

  StravaAuthCallbackController.$inject = ['$location', 'Snackbar', 'Profile', 'Authentication', 'Strava'];

  /**
  * @namespace StravaAuthCallbackController
  */
  function StravaAuthCallbackController($location, Snackbar, Profile, Authentication, Strava) {
    var vm = this;

    vm.code = $location.search().code;

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf mycyclediary.strava.controllers.StravaAuthCallbackController
    */
    function activate() {
      var authenticatedAccount = Authentication.getAuthenticatedAccount();

      // Redirect if not logged in
      if (!authenticatedAccount) {
        $location.url('/');
        Snackbar.error('You are not authorized to view this page.');
      } else {
        Strava.token_exchange(vm.code).then(exchangeSuccessFn, exchangeErrorFn)

        function exchangeSuccessFn(data, status, headers, config) {
          $location.url('/profile')
        }

        function exchangeErrorFn(data,status,headers,config) {
          Snackbar.error(data.data.message);
        }
      }
    }
  }
})();
