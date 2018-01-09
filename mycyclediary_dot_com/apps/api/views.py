import logging, json, datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout

from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from rest_framework.decorators import api_view, detail_route

from mycyclediary_dot_com.apps.strava.models import athlete,component
from mycyclediary_dot_com.apps.strava.strava import strava
from mycyclediary_dot_com.apps.api.serializers import AthleteSerializer,ComponentSerializer,BikeStatSerializer
from mycyclediary_dot_com.apps.api.permissions import IsAthleteOwner

@api_view()
def index(request):
    return HttpResponse('Hello, API is alive!')

@api_view(['GET','POST'])
def strava_webhook_callback(request):
    response = HttpResponse()
    logger = logging.getLogger(__name__)
    logger.debug("Received Strava Webhook API Request")

    # This is a subscribe validation request
    if request.method == 'GET':
        logger.debug("Strava webhook validation request.. {}".format(json.dumps(request.GET)))
        if 'hub.mode' in request.GET and request.GET['hub.mode'] == 'subscribe':
            obj = {
                "hub.challenge": request.GET['hub.challenge']
            }
            response.write(json.dumps(obj))

    # This is an actual callback
    if request.method == 'POST':
        logger.debug("Got a strava callback.. {}".format(json.dumps(request.data)))
        response.write('Yay, thanks for the callback!')

    return response

class AthleteViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'
    queryset = athlete.objects.all()
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
            athlete.objects.create_user(**serializer.validated_data)

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
        queryset = self.queryset.filter(athlete=self.request.user)
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
