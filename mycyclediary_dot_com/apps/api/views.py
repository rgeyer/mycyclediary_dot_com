import logging, json, datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout

from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from rest_framework.decorators import api_view, detail_route, list_route

from stravalib.client import Client

from requests.exceptions import *

from mycyclediary_dot_com.settings.secrets import *
from mycyclediary_dot_com.apps.strava.models import Athlete,component
from mycyclediary_dot_com.apps.strava.strava import strava
from mycyclediary_dot_com.apps.api.serializers import AthleteSerializer,ComponentSerializer,BikeStatSerializer
from mycyclediary_dot_com.apps.api.permissions import IsAthleteOwner

class StravaViewSet(viewsets.ViewSet):
    def get_permissions(self):
        return (permissions.IsAuthenticated(),)

    @list_route(methods=['get','post'])
    def webhook(self, request):
        logger = logging.getLogger(__name__)
        logger.debug("Received Strava Webhook API Request")

        # This is a subscribe validation request
        if request.method == 'GET':
            logger.debug("Strava webhook validation request.. {}".format(json.dumps(request.query_params)))
            if 'hub.mode' in request.query_params and 'hub.challenge' in request.query_params:
                if request.query_params['hub.mode'] == 'subscribe':
                    obj = {
                        "hub.challenge": request.query_params['hub.challenge']
                    }
                    return Response(obj)
                else:
                    return Response({
                        'status': 'Bad Request',
                        'message': 'Invalid hub.mode {}'.format(request.query_params['hub.mode'])
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'status': 'Bad Request',
                    'message': 'Validation request requires query parameters named "hub.mode" and "hub.challenge"'
                }, status=status.HTTP_400_BAD_REQUEST)

        # This is an actual callback
        if request.method == 'POST':
            logger.debug("Got a strava callback.. {}".format(json.dumps(request.data)))
            return Response({"Yay, thanks for the webhook"})

        return Response()

    @list_route(methods=['post'])
    def token_exchange(self, request):
        if 'code' in request.data:
            try:
                strava_client = Client()
                response = strava_client.exchange_code_for_token(SOCIAL_AUTH_STRAVA_KEY, SOCIAL_AUTH_STRAVA_SECRET, request.data['code'])
                leet = Athlete.objects.get(pk=request.user.pk)
                leet.strava_api_token = response
                leet.save()
            except HTTPError as e:
                code = e.args[0][:3]
                message = e.args[0][3:]
                return Response({
                    'status': code,
                    'message': message
                }, status=int(code))
        else:
            return Response({
                'status': 'Bad Request',
                'message': '"code" is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status.HTTP_201_CREATED)

    @list_route(methods=['get'])
    def deauthorize(self, request):
        if request.user.strava_api_token:
            try:
                strava_client = Client(access_token=request.user.strava_api_token)
                response = strava_client.deauthorize()
                request.user.strava_api_token = None
                request.user.save()
            except HTTPError as e:
                code = e.args[0][:3]
                message = e.args[0][3:]
                return Response({
                    'status': code,
                    'message': message
                }, status=int(code))
        else:
            return Response({
                'status': 'Bad Request',
                'message': 'User does not have a valid Strava access_token.'
            }, status.HTTP_400_BAD_REQUEST)

        return Response({}, status.HTTP_204_NO_CONTENT)

class AthleteViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.IsAuthenticated(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return(permissions.IsAuthenticated(), IsAthleteOwner(),)

    def create(self, request):
        request.data['username'] = request.data['email']
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Athlete.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.' # TODO: Send back the serializer.errors, and display them somehow.
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(self.queryset, pk=self.request.user.pk)
        queryset.is_active = False
        queryset.save()

        serializer = self.serializer_class(queryset)

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        queryset = self.queryset.filter(pk=self.request.user.pk)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if str(pk) != str(self.request.user.pk):
            return Response({'status': 'Forbidden', 'message':'You may only access your own athlete record pk={}'.format(self.request.user.pk)},status=status.HTTP_403_FORBIDDEN)
        queryset = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(queryset)

        return Response(serializer.data)

    # TODO: Need to customize the update and partial_update to validate that
    # password and confirm password match, and possibly require the current
    # password in order to allow the change. Other impacted areas are the
    # serializer (mycyclediary_dot_com.apps.api.serializers.AthleteSerializer)
    # and the angular UI which should (pre)validate that the new password and
    # confirm password match.

class ComponentViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'
    queryset = component.objects.all()
    serializer_class = ComponentSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        return(permissions.IsAuthenticated(),)

    def list(self, request):
        # athlete=self.request.user,gear__isnull=False,gear__bike__isnull=False
        filters={"athlete": self.request.user}
        if 'filter' in request.query_params:
            for f in str.split(request.query_params['filter'],','):
                tuples=str.split(f, '=')
                key = tuples[0]
                value = tuples[-1]
                if key == 'type':
                    if value == 'bike':
                        filters.update({"gear__isnull":False,"gear__bike__isnull":False})
                    elif value == 'shoe':
                        filters.update({"gear__isnull":False,"gear__shoe__isnull":False})
                    elif value == 'component':
                        filters.update({"gear__isnull":True})
                    else:
                        return Response({
                            'status': 'Bad request',
                            'message': 'Can not filter by type "{}". Possible type filters are [bike,shoe,component]'.format(value)
                        }, status=status.HTTP_400_BAD_REQUEST)


        queryset = self.queryset.select_related().filter(**filters)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(self.queryset, athlete=self.request.user, pk=pk)
        serializer = self.serializer_class(queryset)

        return Response(serializer.data)

    @detail_route(methods=['post'])
    def aggregates(self, request, pk=None):
        start_date = None
        end_date = None
        if 'start_date' in request.data.keys():
            start_date = datetime.datetime.strptime(request.data['start_date'],"%Y-%m-%dT%H:%M:%S.%fZ")
        if 'end_date' in request.data.keys():
            end_date = datetime.datetime.strptime(request.data['end_date'],"%Y-%m-%dT%H:%M:%S.%fZ")

        component = get_object_or_404(self.queryset, athlete=self.request.user, pk=pk)
        serializer = BikeStatSerializer(component.get_aggregates(start_date=start_date, end_date=end_date))

        return Response(serializer.data)

class LoginView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)

        email = data.get('email', None)
        password = data.get('password', None)

        account = authenticate(username=email, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = AthleteSerializer(account)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Email/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class ActivityViewSet(viewsets.ViewSet):
    def get_permissions(self):
        return (permissions.IsAuthenticated(),)

    def list(self, request):
        stra = strava()
        filters = [
            {'field': 'athlete.id', 'query': int(request.user.strava_id)}
        ]
        activity_cursor = stra.get_activities_mongo(filters)
        activities = []
        for activity in activity_cursor:
            activities.append(activity)
        return Response(activities, status=status.HTTP_200_OK)
