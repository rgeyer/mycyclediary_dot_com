from django.db import models
from django.contrib.auth.models import AbstractUser

class athlete(AbstractUser):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    strava_id = models.PositiveIntegerField(blank=True,null=True,db_index=True)
    last_strava_sync = models.DateTimeField(blank=True,null=True)
    last_api_callback = models.DateTimeField(blank=True,null=True)
    strava_api_token = models.CharField(blank=True,null=True,max_length=64)
    # This apparently also get's a "gear_set" associated with it somewhere.
    # That happens only on new logins, and needs to be updated. Maybe this needs
    # to be checked dynamically?
    # Ahhh this is how that happens.. https://github.com/omab/python-social-auth/blob/v0.2.14/social/backends/strava.py

class component(models.Model):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    athlete = models.ForeignKey(athlete, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(blank=True,null=True,max_length=255)
    brand_name = models.CharField(blank=True,null=True,max_length=255)
    model_name = models.CharField(blank=True,null=True,max_length=255)
    notes = models.TextField(blank=True,null=True)
    aquisition_date = models.DateTimeField(blank=True,null=True)
    aquisition_distance_meters = models.FloatField(blank=False,null=False)
    retire_date = models.DateTimeField(blank=True,null=True)
    battery_type = models.PositiveSmallIntegerField(null=False,blank=False,default=1)

    # Battery type "constants"
    BATTERY_TYPE_UNKNOWN = 0
    BATTERY_TYPE_NONE = 1
    BATTERY_TYPE_RECHARGEAGBLE = 2
    BATTERY_TYPE_REPLACEABLE = 3

    battery_types = {
        BATTERY_TYPE_UNKNOWN: 'Unknown',
        BATTERY_TYPE_NONE: 'None',
        BATTERY_TYPE_RECHARGEAGBLE: 'Rechargeable',
        BATTERY_TYPE_REPLACEABLE: 'Replaceable'
    }

    def battery_str(self):
        try:
            batt_type = component.battery_types[self.battery_type]
            return batt_type
        except KeyError:
            return component.battery_types[component.BATTERY_TYPE_UNKNOWN]


    def isGear(self):
        try:
            # Just access it
            foo = self.gear
            return True
        except:
            return False

    def __str__(self):
        return self.name

class gear(component):
    strava_id = models.CharField(max_length=16,db_index=True,blank=True,null=True)
    primary = models.BooleanField(default=False)
    resource_state = models.PositiveSmallIntegerField(null=True)
    frame_type = models.PositiveSmallIntegerField(null=True,blank=True)

    def isBike(self):
        try:
            # Just access it
            foo = self.bike
            return True
        except:
            return False

    def isShoe(self):
        try:
            # Just access it
            foo = self.shoe
            return True
        except:
            return False

class bike(gear):
    pass

class shoe(gear):
    pass

class activity_component(models.Model):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    athlete = models.ForeignKey(athlete, on_delete=models.CASCADE)
    activity_id = models.BigIntegerField(blank=False,null=False,db_index=True)
    component = models.ForeignKey('component',blank=True,null=True,on_delete=models.SET_NULL)

# This is used to determine "default" components associated with a particular
# parent component, or gear (bike) for a given timespan.
#
# A particular component or component group may be associated with more than one
# parent component or bike for a given time. I.E. I use my Stages PM on both
# my TT bike and my roadbike, and move them between those bikes. Thus that
# component may be "associated" with both bikes for all time.
class component_component(models.Model):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    athlete = models.ForeignKey(athlete, on_delete=models.CASCADE)
    component = models.ForeignKey('component',on_delete=models.CASCADE,related_name='child_component_set')
    start_date = models.DateTimeField(blank=False,null=False)
    end_date = models.DateTimeField(blank=True,null=True)
    parent_component = models.ForeignKey('component',blank=True,null=True,on_delete=models.SET_NULL,related_name='parent_component_set')
