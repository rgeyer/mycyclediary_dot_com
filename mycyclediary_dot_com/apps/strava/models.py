# _*_ coding: utf-8 _*_
"""Django Models for the "strava" sub-app of mycyclediary_dot_com"""
import urllib
import os
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, BaseUserManager
from mycyclediary_dot_com.settings.secrets import SOCIAL_AUTH_STRAVA_KEY
from mycyclediary_dot_com.apps.strava.strava import strava as stra
from mycyclediary_dot_com.apps.core.data import bike_stats

class AthleteManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        athlete = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )

        athlete.set_password(password)
        athlete.save()

        return athlete

    def create_superuser(self, email, password, **kwargs):
        athlete = self.create_user(email, password, **kwargs)

        athlete.is_admin = True
        athlete.save()

        return athlete

class Athlete(AbstractUser):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    strava_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    last_strava_sync = models.DateTimeField(blank=True, null=True)
    last_api_callback = models.DateTimeField(blank=True, null=True)
    strava_api_token = models.CharField(blank=True, null=True, max_length=64)

    objects = AthleteManager()

    def strava_auth_redirect_uri(self):
        strava_auth_uri = "https://www.strava.com/oauth/authorize"
        params = {
            "client_id": SOCIAL_AUTH_STRAVA_KEY,
            "redirect_uri": "https://{}/strava/authcallback".\
                format(os.environ.get('VIRTUAL_HOST', 'localhost')),
            "response_type": "code",
            "scope": "view_private"
        }
        return "{}?{}".format(strava_auth_uri, urllib.parse.urlencode(params))

    def strava_connected(self):
        return self.strava_api_token != None

class Component(models.Model):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(blank=True, null=True, max_length=255)
    brand_name = models.CharField(blank=True, null=True, max_length=255)
    model_name = models.CharField(blank=True, null=True, max_length=255)
    notes = models.TextField(blank=True, null=True)
    aquisition_date = models.DateTimeField(blank=True, null=True)
    aquisition_distance_meters = models.FloatField(blank=False, null=False)
    retire_date = models.DateTimeField(blank=True, null=True)
    battery_type = models.PositiveSmallIntegerField(null=False, blank=False, default=1)

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

    def find_bike(self):
        if self.isGear() and self.gear.isBike():
            return self
        else:
            for bComp in self.parent_component_set.all():
                if bComp.parent_component.isGear() and bComp.parent_component.gear.isBike():
                    return bComp.parent_component
                else:
                    return bComp.parent_component.find_bike()

    def get_aggregates(self, strava=None, start_date=None, end_date=None):
        if not strava:
            strava = stra()
        bike = self.find_bike()
        if bike == self:
            return strava.get_bike_stats(
                self.athlete.strava_id,
                self.gear.strava_id,
                start_date=start_date,
                end_date=end_date
            )
        else:
            aggs = bike_stats()
            # Find all time frames where this component was associated with a
            # bike, or with a parent component which was associated with a bike
            for comp_association in self.parent_component_set.all():
                adjusted_start = comp_association.start_date
                if start_date and start_date > adjusted_start:
                    adjusted_start = start_date

                adjusted_end = comp_association.end_date if comp_association.end_date else end_date
                if end_date and end_date < adjusted_end:
                    adjusted_end = end_date

                bike = comp_association.component.find_bike()
                this_aggs = strava.get_bike_stats(
                    bike.athlete.strava_id,
                    bike.gear.strava_id,
                    adjusted_start,
                    adjusted_end
                )
                aggs = aggs + this_aggs

            return aggs

    def battery_str(self):
        try:
            batt_type = Component.battery_types[self.battery_type]
            return batt_type
        except KeyError:
            return Component.battery_types[Component.BATTERY_TYPE_UNKNOWN]

    def isGear(self):
        try:
            # Just access it
            foo = self.gear
            return True
        except:
            return False

    def isBike(self):
        if self.isGear():
            try:
                foo = self.gear.bike
                return True
            except:
                return False
        else:
            return False

    def isShoe(self):
        if self.isGear():
            try:
                foo = self.gear.shoe
                return True
            except:
                return False
        else:
            return False

    def __str__(self):
        return self.name

    def get_activity_manifest(self, date, profile=None):
        """Returns *this* component, and all (non recursive) child components
        of this component for the specified date.

        Args:
            date (datetime): The datetime of an activity for which a component
                manifest should be returned.
            profile (:obj:`GearComponentProfile`, optional): A component
                profile which should be used to filter/substitute which
                components to use.

        Returns:
            :obj:`list` of :obj:`component` including *this* component, and all
                (non recursive) child components for the specified `date`,
                modified by the specified `profile`
        """
        component_relationships = self.child_component_set.filter(
            Q(start_date__lte=date),
            Q(end_date__isnull=True) | Q(end_date__gte=date)
        )
        components = []
        for component_rel in component_relationships:
            components.append(component_rel.component)

        # Add and remove once, for top level compoments (different wheelset)
        if profile:
            for add in profile.add_components.all():
                components.append(add)

            for remove in profile.remove_components.all():
                if remove in components:
                    components.remove(remove)

        ret_components = components
        for cmp in components:
            # Note: Don't share the profile with the sub-component, since added
            # components will be recusively (and infinitely) added. Instead,
            # apply the profile after the recursive spelunking.
            for child in cmp.get_activity_manifest(date):
                if child not in ret_components:
                    ret_components.append(child)

        # Remove once more, to catch anything the profile might pull off
        if profile:
            for remove in profile.remove_components.all():
                if remove in ret_components:
                    ret_components.remove(remove)

        # Finally add myself
        ret_components.append(self)

        return ret_components

class Gear(Component):
    strava_id = models.CharField(max_length=16, db_index=True, blank=True, null=True)
    primary = models.BooleanField(default=False)
    resource_state = models.PositiveSmallIntegerField(null=True)
    frame_type = models.PositiveSmallIntegerField(null=True, blank=True)

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

class Bike(Gear):
    pass

class Shoe(Gear):
    pass

class GearComponentProfile(models.Model):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    gear = models.ForeignKey(Gear, on_delete=models.CASCADE)
    add_components = models.ManyToManyField(Component, related_name='profile_add_components')
    remove_components = models.ManyToManyField(Component, related_name='profile_remove_components')

# This is used to determine "default" components associated with a particular
# parent component, or gear (bike) for a given timespan.
#
# A particular component or component group may be associated with more than one
# parent component or bike for a given time. I.E. I use my Stages PM on both
# my TT bike and my roadbike, and move them between those bikes. Thus that
# component may be "associated" with both bikes for all time.
class ComponentComponent(models.Model):
    class Meta:
        app_label = 'mycyclediary_dot_com'

    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    component = models.ForeignKey('Component', on_delete=models.CASCADE, related_name='parent_component_set')
    start_date = models.DateTimeField(blank=False, null=False)
    end_date = models.DateTimeField(blank=True, null=True)
    parent_component = models.ForeignKey('Component', blank=True, null=True, on_delete=models.SET_NULL, related_name='child_component_set')

class Activity():
    """A model/helper class for Strava activities stored in mongodb. This is most
    certainly *NOT* a Django ORM model, but it seems to make sense to keep it in
    this module.
    """
