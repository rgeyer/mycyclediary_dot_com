from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from mycyclediary_dot_com.apps.strava.models import athlete, component

class AthleteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        return athlete.objects.create(**validated_data)

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
        model = athlete
        fields = ('id', 'email', 'username', 'date_joined', 'last_login',
                  'first_name', 'last_name', 'password', 'is_superuser',
                  'is_staff', 'is_active', 'last_strava_sync', 'strava_id',
                  'confirm_password', 'strava_auth_redirect_uri', 'strava_connected',)
        read_only_fields = ('strava_id','strava_auth_redirect_uri', 'strava_connected',)

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = component

        fields =    ('id', 'name', 'description', 'brand_name',
                    'model_name', 'notes', 'aquisition_date',
                    'aquisition_distance_meters', 'retire_date',
                    'battery_type', 'battery_str', 'isBike',)
        read_only_fields = ('id','battery_str','isBike',)

class BikeStatSerializer(serializers.Serializer):
    meters_distance = serializers.FloatField()
    time = serializers.IntegerField()
    meters_elevation = serializers.FloatField()
    meters_per_second_avg_speed = serializers.FloatField()
    kjs = serializers.IntegerField()
