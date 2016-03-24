from django.db import models
from django.contrib.auth.models import AbstractUser

class athlete(AbstractUser):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    strava_id = models.PositiveIntegerField(blank=True,null=True)
    last_strava_sync = models.DateTimeField(blank=True,null=True)
    strava_api_token = models.CharField(blank=True,null=True,max_length=64)

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
