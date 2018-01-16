(function () {
  'use strict';

  angular
    .module('mycyclediary.routes')
    .config(config);

  config.$inject = ['$routeProvider'];

  /**
  * @name config
  * @desc Define valid application routes
  */
  function config($routeProvider) {
    $routeProvider.when('/signup', {
      controller: 'RegisterController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/signup.html'
    }).when('/login', {
      controller: 'LoginController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/login.html'
    }).when('/profile', {
      controller: 'ProfileController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/profiles/profile.html'
    }).when('/profile/settings', {
      controller: 'ProfileSettingsController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/profiles/settings.html'
    }).when('/activities', {
      controller: 'ActivitiesController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/activities/index.html'
    }).when('/components', {
      controller: 'AthleteComponentController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/component/athlete-components.html'
    }).when('/strava/authcallback', {
      controller: 'StravaAuthCallbackController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/strava/authcallback.html'
    }).otherwise('/');
  }
})();
