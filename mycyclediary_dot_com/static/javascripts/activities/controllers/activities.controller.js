/**
* ActivitiesController
* @namespace mycyclediary.activites.controllers
*/
(function () {
  'use strict';

  angular
    .module('mycyclediary.activities.controllers')
    .controller('ActivitiesController', ActivitiesController);

  ActivitiesController.$inject = ['$location', '$scope', '$q', '$http', 'Snackbar', 'DTOptionsBuilder', 'DTColumnBuilder'];

  /**
  * @namespace ActivitiesController
  */
  function ActivitiesController($location, $scope, $q, $http, Snackbar, DTOptionsBuilder, DTColumnBuilder) {
    var vm = this;

    vm.dtOptions = DTOptionsBuilder.fromFnPromise(function() {
        var defer = $q.defer();
        $http.get('/api/activities/').then(function(result) {
            defer.resolve(result.data);
        });
        return defer.promise;
    }).withPaginationType('full_numbers');

    vm.dtColumns = [
        DTColumnBuilder.newColumn('start_date_local').withTitle('Date'),
        DTColumnBuilder.newColumn('type').withTitle('Type'),
        DTColumnBuilder.newColumn('name').withTitle('Name'),
        DTColumnBuilder.newColumn('distance').withTitle('Distance'),
        DTColumnBuilder.newColumn('elapsed_time').withTitle('Time')
    ];
  }
})();
