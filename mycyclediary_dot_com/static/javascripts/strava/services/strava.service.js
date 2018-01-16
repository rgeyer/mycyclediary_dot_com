/**
* Strava
* @namespace mycyclediary.strava.services
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.strava.services')
    .factory('Strava', Strava);

  Strava.$inject = ['$http'];

  /**
  * @namespace Strava
  */
  function Strava($http) {
    /**
    * @name Strava
    * @desc The factory to be returned
    * @memberOf mycyclediary.strava.services.Strava
    */
    var Strava = {
      token_exchange: token_exchange,
      deauthorize: deauthorize,
    };

    return Strava;

    /////////////////////

    /**
    * @name token_exchange
    * @desc Exchange an oauth code for an access token
    * @param {string} code The code produced by an oauth request
    * @returns {Promise}
    * @memberOf mycylediary.strava.services.Strava
    * @see http://strava.github.io/api/partner/v3/oauth/#get-authorize
    */
    function token_exchange(code) {
      return $http.post('/api/strava/token_exchange/', {code: code});
    }

    /**
    * @name deauthorize
    * @desc Deauthorizes the strava user
    * @returns {Promise}
    * @memberOf mycylediary.strava.services.Strava
    * @see http://strava.github.io/api/partner/v3/oauth/#deauthorize
    */
    function deauthorize() {
      return $http.get('/api/strava/deauthorize/');
    }
  }
})();
