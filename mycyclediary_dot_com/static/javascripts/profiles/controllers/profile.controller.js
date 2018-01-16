/**
* ProfileController
* @namespace mycyclediary.profiles.controllers
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.profiles.controllers')
    .controller('ProfileController', ProfileController);

  ProfileController.$inject = ['$location', '$routeParams', 'Authentication', 'Profile', 'Snackbar', 'Strava'];

  /**
  * @namespace ProfileController
  */
  function ProfileController($location, $routeParams, Authentication, Profile, Snackbar, Strava) {
    var vm = this;

    vm.profile = undefined;
    vm.posts = [];

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf mycyclediary.profiles.controllers.ProfileController
    */
    function activate() {
      var authenticatedAccount = Authentication.getAuthenticatedAccount();

      // Redirect if not logged in
      if (!authenticatedAccount) {
        $location.url('/');
        Snackbar.error('You are not authorized to view this page.');
      }

      Profile.get(authenticatedAccount.id).then(profileSuccessFn, profileErrorFn);

      /**
      * @name profileSuccessProfile
      * @desc Update `profile` on viewmodel
      */
      function profileSuccessFn(data, status, headers, config) {
        vm.profile = data.data;
      }


      /**
      * @name profileErrorFn
      * @desc Redirect to index and show error Snackbar
      */
      function profileErrorFn(data, status, headers, config) {
        $location.url('/');
        Snackbar.error('That user does not exist.');
      }
    }

    vm.strava_deauthorize = function() {
      Strava.deauthorize().then(deauthorizeSuccessFn, deauthorizeErrorFn)

      function deauthorizeSuccessFn(data, status, headers, config) {
        vm.profile.strava_connected = false;
      }

      function deauthorizeErrorFn(data,status,headers,config) {
        Snackbar.error(data.data.message);
      }
    }
  }
})();
