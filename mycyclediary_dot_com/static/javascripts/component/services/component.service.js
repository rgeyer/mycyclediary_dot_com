/**
* Profile
* @namespace mycyclediary.component.services
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.component.services')
    .factory('Component', Component);

  Component.$inject = ['$http'];

  /**
  * @namespace Component
  */
  function Component($http) {
    /**
    * @name Component
    * @desc The factory to be returned
    * @memberOf mycyclediary.component.services.Component
    */
    var Component = {
      all: all,
    };

    return Component;

    /////////////////////

    /**
    * @name all
    * @desc Get all Components
    * @returns {Promise}
    * @memberOf mycylediary.component.services.Component
    */
    function all() {
      return $http.get('/api/components/');
    }
  }
})();
