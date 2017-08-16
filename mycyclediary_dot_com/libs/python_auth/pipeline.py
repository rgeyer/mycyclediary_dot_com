from mycyclediary_dot_com.apps.strava.tasks import *
import logging

def user_details(strategy, details, user=None, *args, **kwargs):

    if user:
        updated = False
        if user.social_auth:
            provider = user.social_auth.get(provider='strava')
            if provider:
                user.strava_id = provider.uid
                # The username should be the email
                user.username = user.email
                updated = True
                if 'access_token' in provider.extra_data.keys():
                    user.strava_api_token = user.social_auth.get(provider='strava').extra_data['access_token']

        if updated:
            strategy.storage.user.changed(user)

def first_sync(strategy, details, user=None, *args, **kwargs):

    if user:
        if not user.last_strava_sync:
            try:
                update_athlete.delay(user)
            except:
                pass
                # TODO: Maybe try harder and catch real issues?
                # I hate to do this, but this would be the worst place
                # for a user to have a bad experience.
                #
                # rabbitmq down:
                # raise socket.error(last_err)
                # socket.error: [Errno 111] Connection refused
