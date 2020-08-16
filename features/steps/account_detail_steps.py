from behave import *
from features.steps.base_steps import *


@when('I get account details of current logged in user')
def step_impl(context):
    url = '3/account/' + context.logged_in_username
    set_auth_header(context, 'Client-ID ' + context.client_id)
    get_request(context, url)


@then('I verify the account details and user id should be {user_id}')
def step_impl(context, user_id):
    assert context.response.json()['data']['url'] == context.logged_in_username
    assert not context.response.json()['data']['is_blocked']
    assert context.response.json()['data']['id'] == int(user_id)


@when('I update username as {username}')
def step_impl(context, username):
    url = '3/account/' + context.logged_in_username + '/settings'
    set_auth_header(context, context.access_token)
    put_request(context, url, {'username': username})
    context.logged_in_username = username
