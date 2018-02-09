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
      create: create,
      get: get,
      aggregates: aggregates,
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

    function create(component_type, name, description, brand_name, model_name, notes, aquisition_date, aquisition_distance_meters, retire_date, battery_type) {
      return $http.post('/api/components/',{
        component_type: component_type,
        name: name,
        description: description,
        brand_name: brand_name,
        model_name: model_name,
        notes: notes,
        aquisition_date: aquisition_date,
        aquisition_distance_meters: aquisition_distance_meters,
        retire_date: retire_date,
        battery_type: battery_type
      });
    }

    function get(id) {
      return $http.get('/api/components/{}/'+id);
    }

    function aggregates(id, start_date, end_date) {
      return $http.post('/api/components/'+id+'/aggregates/', {start_date: start_date, end_date: end_date});
    }
  }
})();
