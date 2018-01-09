import pytz
from datetime import datetime
from mycyclediary_dot_com.models import *
from mycyclediary_dot_com.apps.strava.strava import strava

def test_get_bike_stats_no_date_limits(mongodb):
    stra = strava(mongodb=mongodb)
    stats = stra.get_bike_stats(1,'3')
    assert stats.meters_distance > 0.0
    assert stats.records == 10

def test_get_bike_stats_only_start_date(mongodb):
    start_date = datetime.strptime('2017-10-09T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    start_date = start_date.replace(tzinfo=pytz.UTC)
    stra = strava(mongodb=mongodb)
    stats = stra.get_bike_stats(1,'3',start_date=start_date)
    assert stats.meters_distance > 0
    assert stats.records == 9

def test_get_bike_stats_only_end_date(mongodb):
    end_date = datetime.strptime('2017-10-17T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    end_date = end_date.replace(tzinfo=pytz.UTC)
    stra = strava(mongodb=mongodb)
    stats = stra.get_bike_stats(1,'3',end_date=end_date)
    assert stats.meters_distance > 0
    assert stats.records == 9

def test_get_bike_stats_start_and_end_date(mongodb):
    start_date = datetime.strptime('2017-10-09T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    start_date = start_date.replace(tzinfo=pytz.UTC)
    end_date = datetime.strptime('2017-10-17T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    end_date = end_date.replace(tzinfo=pytz.UTC)
    stra = strava(mongodb=mongodb)
    stats = stra.get_bike_stats(1,'3',start_date=start_date,end_date=end_date)
    assert stats.meters_distance > 0
    assert stats.records == 8

def test_get_bike_stats_athlete_filter(mongodb):
    stra = strava(mongodb=mongodb)
    stats = stra.get_bike_stats(1,'3')
    assert stats.records == 10
    stats = stra.get_bike_stats(2,'3')
    assert stats.records == 10

def test_get_bike_stats_bike_filter(mongodb):
    stra = strava(mongodb=mongodb)
    stats = stra.get_bike_stats(1,'3')
    assert stats.records == 10
    stats = stra.get_bike_stats(1,'4')
    assert stats.records == 10
