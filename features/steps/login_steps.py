from behave import *
from features.steps.base_steps import *


def user_credentials(value=None):
    return file_helper('authorization_keys', value)


def set_user_credentials(context, username):
    registered_users = user_credentials()
    if username in registered_users.keys():
        context.client_id = registered_users[username]['client_id']
        context.client_secret = registered_users[username]['client_secret']
        context.refresh_token = registered_users[username]['refresh_token']
    else:
        # Not implemented properly, don't know if this needs to be done as part of test setup
        # but we can do it something like this
        if context.config.userdata.getbool('CAN_REGISTER_USER', False):
            # STEP1: Post call to register user
            # STEP2: Add client to user
            request_body = {'auth_callback_url': context.auth_callback_url}
            post_request(context, '/oauth2/addclient', request_body)
            context.client_id = context.response.json()['client_id']
            context.client_secret = context.response.json()['client_secret']
            # We can make similar calls to get auth access tokens
            # and write in file to use it for further sessions like following
            registered_users(
                {username: {'auth_callback_url': context.auth_callback_url,
                            'client_id': context.client_id, 'client_secret': context.client_secret
                            }
                 }
            )
        else:
            print('*********************User Not Registered\n')
            assert False


@given('I am logged in as {username}')
def step_impl(context, username):
    set_user_credentials(context, username)
    request_body = {'refresh_token': context.refresh_token, 'client_id': context.client_id,
                    'client_secret': context.client_secret, 'grant_type': 'refresh_token'}
    post_request(context, '/oauth2/token', request_body)
    context.access_token = 'Bearer ' + context.response.json()['access_token']
    context.logged_in_username = context.response.json()['account_username']


@when('I logout and login as {username}')
def step_impl(context, username):
    # Didn't find the api for logout, so just logging in as new user
    context.execute_steps(u'''
        given I am logged in as {user}
    '''.format(user=username))
