import pytz
from datetime import datetime
from mycyclediary_dot_com.models import *
from mycyclediary_dot_com.apps.strava.strava import strava

def test_battery_str_returns_unknown():
    comp = Component(athlete_id=1,name="foo",battery_type=9)
    assert comp.battery_str() == Component.battery_types[Component.BATTERY_TYPE_UNKNOWN]

def test_can_find_bike_when_component_is_bike(db, django_db_setup):
    comp = Component.objects.get(pk=3)
    assert comp.find_bike() == comp

def test_can_find_bike_when_component_is_child_of_bike(db, django_db_setup):
    bike = Component.objects.get(pk=3)
    comp = Component.objects.get(pk=1)
    assert comp.find_bike() == bike

def test_aggregate_on_bike(db, django_db_setup, mongodb):
    bike = Component.objects.get(pk=3)
    stra = strava(mongodb=mongodb)
    aggregates = bike.get_aggregates(strava=stra)
    assert aggregates.records == 10
    assert aggregates.meters_distance == 160934.4
    assert aggregates.time == 18000
    assert aggregates.meters_elevation == 5000
    assert aggregates.kjs == 10000
    assert aggregates.meters_per_second_avg_speed > 8.0

def test_aggregate_on_wheelset1(db, django_db_setup, mongodb):
    bike = Component.objects.get(pk=1)
    assert bike.parent_component_set.all().count() > 0
    stra = strava(mongodb=mongodb)
    aggregates = bike.get_aggregates(strava=stra)
    assert aggregates.records == 10
    assert aggregates.meters_distance == 160934.4
    assert aggregates.time == 18000
    assert aggregates.meters_elevation == 5000
    assert aggregates.kjs == 10000
    assert aggregates.meters_per_second_avg_speed > 8.0

def test_aggregate_on_wheelset2(db, django_db_setup, mongodb):
    bike = Component.objects.get(pk=2)
    assert bike.parent_component_set.all().count() == 0
    stra = strava(mongodb=mongodb)
    aggregates = bike.get_aggregates(strava=stra)
    assert aggregates.records == 0

def test_aggregate_on_bike_start_date(db, django_db_setup, mongodb):
    start_date = datetime.strptime('2017-10-09T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    start_date = start_date.replace(tzinfo=pytz.UTC)
    bike = Component.objects.get(pk=3)
    stra = strava(mongodb=mongodb)
    aggregates = bike.get_aggregates(strava=stra,start_date=start_date)
    assert aggregates.records == 9
    assert aggregates.meters_distance == 16093.44 * 9
    assert aggregates.time == 1800 * 9
    assert aggregates.meters_elevation == 500 * 9
    assert aggregates.kjs == 1000 * 9
    assert aggregates.meters_per_second_avg_speed > 8.0

def test_aggregate_on_bike_end_date(db, django_db_setup, mongodb):
    end_date = datetime.strptime('2017-10-17T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    end_date = end_date.replace(tzinfo=pytz.UTC)
    bike = Component.objects.get(pk=3)
    stra = strava(mongodb=mongodb)
    aggregates = bike.get_aggregates(strava=stra,end_date=end_date)
    assert aggregates.records == 9
    assert aggregates.meters_distance == 16093.44 * 9
    assert aggregates.time == 1800 * 9
    assert aggregates.meters_elevation == 500 * 9
    assert aggregates.kjs == 1000 * 9
    assert aggregates.meters_per_second_avg_speed > 8.0

def test_aggregate_on_bike_start_date_and_end_date(db, django_db_setup, mongodb):
    start_date = datetime.strptime('2017-10-09T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    start_date = start_date.replace(tzinfo=pytz.UTC)
    end_date = datetime.strptime('2017-10-17T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    end_date = end_date.replace(tzinfo=pytz.UTC)
    bike = Component.objects.get(pk=3)
    stra = strava(mongodb=mongodb)
    aggregates = bike.get_aggregates(strava=stra,start_date=start_date,end_date=end_date)
    assert aggregates.records == 8
    assert aggregates.meters_distance == 16093.44 * 8
    assert aggregates.time == 1800 * 8
    assert aggregates.meters_elevation == 500 * 8
    assert aggregates.kjs == 1000 * 8
    assert aggregates.meters_per_second_avg_speed > 8.0

def test_aggregate_on_wheelset1_start_date(db, django_db_setup, mongodb):
    start_date = datetime.strptime('2017-10-09T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    start_date = start_date.replace(tzinfo=pytz.UTC)
    bike = Component.objects.get(pk=1)
    stra = strava(mongodb=mongodb)
    aggregates = bike.get_aggregates(strava=stra,start_date=start_date)
    assert aggregates.records == 9
    assert aggregates.meters_distance == 16093.44 * 9
    assert aggregates.time == 1800 * 9
    assert aggregates.meters_elevation == 500 * 9
    assert aggregates.kjs == 1000 * 9
    assert aggregates.meters_per_second_avg_speed > 8.0

def test_aggregate_on_wheelset1_end_date(db, django_db_setup, mongodb):
    end_date = datetime.strptime('2017-10-17T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    end_date = end_date.replace(tzinfo=pytz.UTC)
    bike = Component.objects.get(pk=1)
    stra = strava(mongodb=mongodb)
    aggregates = bike.get_aggregates(strava=stra,end_date=end_date)
    assert aggregates.records == 9
    assert aggregates.meters_distance == 16093.44 * 9
    assert aggregates.time == 1800 * 9
    assert aggregates.meters_elevation == 500 * 9
    assert aggregates.kjs == 1000 * 9
    assert aggregates.meters_per_second_avg_speed > 8.0

def test_aggregate_on_wheelset1_start_date_and_end_date(db, django_db_setup, mongodb):
    start_date = datetime.strptime('2017-10-09T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    start_date = start_date.replace(tzinfo=pytz.UTC)
    end_date = datetime.strptime('2017-10-17T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    end_date = end_date.replace(tzinfo=pytz.UTC)
    bike = Component.objects.get(pk=1)
    stra = strava(mongodb=mongodb)
    aggregates = bike.get_aggregates(strava=stra,start_date=start_date,end_date=end_date)
    assert aggregates.records == 8
    assert aggregates.meters_distance == 16093.44 * 8
    assert aggregates.time == 1800 * 8
    assert aggregates.meters_elevation == 500 * 8
    assert aggregates.kjs == 1000 * 8
    assert aggregates.meters_per_second_avg_speed > 8.0

def test_get_gear_manifest_for_activity_no_profile(db, django_db_setup, mongodb):
    activity_date = datetime.strptime('2017-10-12T23:59:59Z', '%Y-%m-%dT%H:%M:%SZ')
    bike_gear = Bike.objects.get(pk=3)
    manifest = bike_gear.get_activity_manifest(activity_date)
    assert len(manifest) == 3
    manifest_ids = []
    for cmp in manifest:
        manifest_ids.append(cmp.id)
    assert manifest_ids.sort() == [3,1,5].sort()

def test_get_gear_manifest_for_activity_with_profile(db, django_db_setup, mongodb):
    activity_date = datetime.strptime('2017-10-12T23:59:59Z', '%Y-%m-%dT%H:%M:%SZ')
    bike_gear = Bike.objects.get(pk=3)
    profile = GearComponentProfile.objects.get(pk=1)
    manifest = bike_gear.get_activity_manifest(activity_date, profile=profile)
    assert len(manifest) == 2
    manifest_ids = []
    for cmp in manifest:
        manifest_ids.append(cmp.id)
    assert manifest_ids.sort() == [3,2].sort()

def test_get_gear_manifest_for_activity_with_profile1(db, django_db_setup, mongodb):
    # This profile should simply exchange the 11-25 cassette for the 11-32
    # cassette
    activity_date = datetime.strptime('2017-10-12T23:59:59Z', '%Y-%m-%dT%H:%M:%SZ')
    bike_gear = Bike.objects.get(pk=3)
    profile = GearComponentProfile.objects.get(pk=2)
    manifest = bike_gear.get_activity_manifest(activity_date, profile=profile)
    assert len(manifest) == 3
    manifest_ids = []
    for cmp in manifest:
        manifest_ids.append(cmp.id)
    assert manifest_ids.sort() == [3,1,6].sort()
