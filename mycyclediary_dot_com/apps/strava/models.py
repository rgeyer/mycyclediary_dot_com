from django.db import models
from django.contrib.auth.models import AbstractUser

class athlete(AbstractUser):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    strava_id = models.PositiveIntegerField(blank=True,null=True)
    last_strava_sync = models.DateTimeField(blank=True,null=True)
    last_api_callback = models.DateTimeField(blank=True,null=True)
    strava_api_token = models.CharField(blank=True,null=True,max_length=64)
    # This apparently also get's a "gear_set" associated with it somewhere.
    # That happens only on new logins, and needs to be updated. Maybe this needs
    # to be checked dynamically?
    # Ahhh this is how that happens.. https://github.com/omab/python-social-auth/blob/v0.2.14/social/backends/strava.py

class gear(models.Model):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    strava_id = models.CharField(max_length=16,primary_key=True)
    athlete = models.ForeignKey(athlete, on_delete=models.CASCADE)
    primary = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    description = models.CharField(blank=True,null=True,max_length=255)
    resource_state = models.PositiveSmallIntegerField(null=True)
    brand_name = models.CharField(blank=True,null=True,max_length=255)
    model_name = models.CharField(blank=True,null=True,max_length=255)
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

class activity_bike(models.Model):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    athlete = models.ForeignKey(athlete, on_delete=models.CASCADE)
    activity_id = models.BigIntegerField(blank=False,null=False)
    bike = models.ForeignKey(bike,blank=True,null=True,on_delete=models.SET_NULL)

class activity_component(models.Model):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    athlete = models.ForeignKey(athlete, on_delete=models.CASCADE)
    activity_id = models.BigIntegerField(blank=False,null=False)
    component = models.ForeignKey('component',blank=True,null=True,on_delete=models.SET_NULL)


# This is used to determine "default" components associated with a particular
# parent component, or gear (bike) for a given timespan.
#
# A particular component or component group may be associated with more than one
# parent component or bike for a given time. I.E. I use my Stages PM on both
# my TT bike and my roadbike, and move them between those bikes. Thus that
# component may be "associated" with both bikes for all time.
class bike_component(models.Model):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    athlete = models.ForeignKey(athlete, on_delete=models.CASCADE)
    component = models.ForeignKey('component',on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=False,null=False)
    end_date = models.DateTimeField(blank=False,null=False)
    parent_component = models.ForeignKey('component',blank=True,null=True,on_delete=models.SET_NULL,related_name='parent_component_set')
    bike = models.ForeignKey(bike,blank=True,null=True,on_delete=models.SET_NULL)


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
    battery_charged = models.DateTimeField(blank=True,null=True)
    battery_replaced = models.DateTimeField(blank=True,null=True)
