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

class strava_webhook_subscription(models.Model):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    athlete = models.ForeignKey(athlete, on_delete=models.CASCADE)
    strava_id = models.PositiveSmallIntegerField(blank=True,null=True)
    object_type = models.CharField(blank=True,null=True,max_length=255)
    aspect_type = models.CharField(blank=True,null=True,max_length=255)
    created_at = models.DateTimeField(blank=True,null=True)
    updated_at = models.DateTimeField(blank=True,null=True)
    verify_token = models.CharField(max_length=32)

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

# class bike_component(models.Model):
#     pass
