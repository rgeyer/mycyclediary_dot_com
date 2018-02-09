from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from mycyclediary_dot_com.apps.strava.models import Athlete, Component, Bike, Shoe

class AthleteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        return Athlete.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.save()

        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
            instance.save()

        request = self.context.get('request')

        if request:
            update_session_auth_hash(request, instance)

        return instance

    class Meta:
        model = Athlete
        fields = ('id', 'email', 'username', 'date_joined', 'last_login',
                  'first_name', 'last_name', 'password', 'is_superuser',
                  'is_staff', 'is_active', 'last_strava_sync', 'strava_id',
                  'confirm_password', 'strava_auth_redirect_uri', 'strava_connected',)
        read_only_fields = ('strava_id', 'strava_auth_redirect_uri', 'strava_connected',)

class ComponentSerializer(serializers.ModelSerializer):
    component_type = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        request = self.context.get('request')
        athlete = request.user

        component_type = validated_data['component_type']
        validated_data.pop('component_type', None)

        if component_type == 'bike':
            new_component = Bike(**validated_data)
        elif component_type == 'shoe':
            new_component = Shoe(**validated_data)
        else:
            new_component = Component(**validated_data)

        new_component.athlete = athlete
        new_component.save()
        return new_component

    def validate_component_type(self, value):
        """
        Ensure that the component type is correct
        """
        if value not in ['bike', 'shoe', 'component']:
            raise serializers.ValidationError(
                "Component type must be 'bike', 'shoe', or 'component'")
        return value

    class Meta:
        model = Component

        fields = ('id', 'name', 'description', 'brand_name', 'model_name',
                  'notes', 'aquisition_date', 'aquisition_distance_meters',
                  'retire_date', 'battery_type', 'battery_str', 'isBike',
                  'isShoe', 'component_type')
        read_only_fields = ('id', 'battery_str', 'isBike', 'isShoe')

class BikeStatSerializer(serializers.Serializer):
    meters_distance = serializers.FloatField()
    time = serializers.IntegerField()
    meters_elevation = serializers.FloatField()
    meters_per_second_avg_speed = serializers.FloatField()
    kjs = serializers.IntegerField()
