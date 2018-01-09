from mycyclediary_dot_com.apps.strava.mongohelper import mongohelper

def test_mongo_fixture_record_count(mongodb):
    assert 'raw_activities_resource_state_2' in mongodb.collection_names()
    records = mongodb.raw_activities_resource_state_2.find()
    record_count = records.count()
    assert record_count == 80
