/**
* Component
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
      bikes: bikes,
      shoes: shoes,
      components: components,
    };

    return Component;

    /////////////////////

    /**
    * @name list
    * @desc Get all Components
    * @returns {Promise}
    * @memberOf mycylediary.component.services.Component
    */
    function list(type) {
      return $http.get('/api/components/?filter=type='+type);
    }

    /**
    * @name all
    * @desc Get all Components
    * @returns {Promise}
    * @memberOf mycylediary.component.services.Component
    */
    function all() {
      return $http.get('/api/components/');
    }

    /**
    * @name bikes
    * @desc Get all bike Components
    * @returns {Promise}
    * @memberOf mycylediary.component.services.Component
    */
    function bikes() {
      return list('bike');
    }

    /**
    * @name shoes
    * @desc Get all shoe Components
    * @returns {Promise}
    * @memberOf mycylediary.component.services.Component
    */
    function shoes() {
      return list('shoe');
    }

    /**
    * @name components
    * @desc Get all non bike or shoe Components
    * @returns {Promise}
    * @memberOf mycylediary.component.services.Component
    */
    function components() {
      return list('component');
    }
  }
})();
