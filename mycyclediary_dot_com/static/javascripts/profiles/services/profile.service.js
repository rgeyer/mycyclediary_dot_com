/**
* Profile
* @namespace mycyclediary.profiles.services
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.profiles.services')
    .factory('Profile', Profile);

  Profile.$inject = ['$http'];

  /**
  * @namespace Profile
  */
  function Profile($http) {
    /**
    * @name Profile
    * @desc The factory to be returned
    * @memberOf mycyclediary.profiles.services.Profile
    */
    var Profile = {
      destroy: destroy,
      get: get,
      update: update
    };

    return Profile;

    /////////////////////

    /**
    * @name destroy
    * @desc Destroys the given profile
    * @param {Object} profile The profile to be destroyed
    * @returns {Promise}
    * @memberOf mycyclediary.profiles.services.Profile
    */
    function destroy(profile) {
      return $http.delete('/api/athletes/' + profile.id + '/');
    }


    /**
    * @name get
    * @desc Gets the profile for user with username `username`
    * @param {string} athlete_id The athlete_id of the user to fetch
    * @returns {Promise}
    * @memberOf mycyclediary.profiles.services.Profile
    */
    function get(athlete_id) {
      return $http.get('/api/athletes/' + athlete_id + '/');
    }


    /**
    * @name update
    * @desc Update the given profile
    * @param {Object} profile The profile to be updated
    * @returns {Promise}
    * @memberOf mycyclediary.profiles.services.Profile
    */
    function update(profile) {
      return $http.put('/api/athletes/' + profile.id + '/', profile);
    }
  }
})();
