from behave_http.steps import *
import json
import pdb, sys


def file_helper(file_name, value=None):
    file_path = './features/global_state/' + file_name + '.py'
    if value:
        existing_value = eval(open(file_path, 'r').read())
        for key in value.keys():
            existing_value[key] = value[key]
        open(file_path, 'w').write(str(existing_value))
    return eval(open(file_path, 'r').read())


def post_request(context, url, body):
    _json = json.dumps(body)
    context.execute_steps(u'''
            when I make a POST request to "{path}"
            """
            {json}
            """
        '''.format(json=_json, path=url))
    assert context.response.status_code == 200


def get_request(context, url, status=200):
    context.execute_steps(u'''
            when I make a GET request to "{path}"
        '''.format(path=url))
    assert context.response.status_code == status


def delete_request(context, url):
    context.execute_steps(u'''
            when I make a DELETE request to "{path}"
        '''.format(path=url))
    assert context.response.status_code == 200


def put_request(context, url, body):
    _json = json.dumps(body)
    context.execute_steps(u'''
            when I make a PUT request to "{path}"
            """
            {json}
            """
        '''.format(json=_json, path=url))
    assert context.response.status_code == 200


def set_auth_header(context, header):
    context.execute_steps(u'''
            given I set "Authorization" header to "{token}"
            '''.format(token=header))
