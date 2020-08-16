from behave import *
from features.steps.base_steps import *


@when('I create a new album called {name}')
def step_impl(context, name):
    set_auth_header(context, context.access_token)
    body = {'title': name, 'description': 'test assignment', 'privacy': 'public'}
    post_request(context, '3/album', body)
    context.album_ids[name] = {'id': context.response.json()['data']['id'], 'images': [], 'comments': []}


@when('I made {name} album public')
def step_impl(context, name):
    set_auth_header(context, context.access_token)
    album_id = context.album_ids[name]['id']
    url = '3/album/' + album_id
    put_request(context, url, {'privacy': 'public'})
    url = '3/gallery/album/' + album_id
    post_request(context, url, {'title': name})


@given('Images are already uploaded')
def step_impl(context):
    set_auth_header(context, context.access_token)
    body = {'image': 'https://martinfowler.com/bliki/images/testPyramid/test-pyramid.png',
            'type': 'url', 'name': 'test-pyramid.png'}
    post_request(context, '3/upload', body)
    assert body['name'] == context.response.json()['data']['name']
    context.uploaded_images[body['name']] = {'id': context.response.json()['data']['id'], 'link': context.response.json()['data']['link']}


@when('I add uploaded images to {name} album')
def step_impl(context, name):
    set_auth_header(context, context.access_token)
    album_id = context.album_ids[name]['id']
    url = '3/album/' + album_id + '/add'
    for image_name in context.uploaded_images.keys():
        post_request(context, url, {'ids': context.uploaded_images[image_name]['id']})
        uploaded_images = context.album_ids[name]['images']
        uploaded_images.append(context.uploaded_images[image_name]['id'])
        context.album_ids[name]['images'] = uploaded_images


@when('I mark {name} album as my favourite')
def step_impl(context, name):
    set_auth_header(context, context.access_token)
    album_id = context.album_ids[name]['id']
    url = '3/album/' + album_id + '/favorite'
    post_request(context, url, {})


@when('I comment {comment} on {album} album')
def step_impl(context, comment, album):
    set_auth_header(context, context.access_token)
    album_id = context.album_ids[album]['id']
    body = {'image_id': album_id, 'comment': comment}
    post_request(context, '3/comment', body)
    comments = context.album_ids[album]['comments']
    comments.append(context.response.json()['data']['id'])
    context.album_ids[album]['comments'] = comments


@when('I access the comments on {album} album and {vote} vote them')
def step_impl(context, album, vote):
    set_auth_header(context, context.access_token)
    comments = context.album_ids[album]['comments']
    for comment in comments:
        url = '3/comment/' + str(comment) + '/vote/' + vote
        post_request(context, url, {})


@then('I verify all the comments has upvote on {album} album')
def step_impl(context, album):
    set_auth_header(context, 'Client-ID ' + context.client_id)
    comments = context.album_ids[album]['comments']
    for comment in comments:
        url = '3/comment/' + str(comment)
        get_request(context, url)
        assert context.response.json()['data']['ups'] > 0


@when('I reply {comment_msg} to the comments on {album} album')
def step_impl(context, comment_msg, album):
    set_auth_header(context, context.access_token)
    album_id = context.album_ids[album]['id']
    comments = context.album_ids[album]['comments']
    for comment in comments:
        body = {'image_id': album_id, 'comment': comment_msg, 'parent_id': comment}
        post_request(context, '3/comment', body)


@then('I verify details of {album} album and it should{flag}be my favourite')
def step_impl(context, album, flag):
    set_auth_header(context, context.access_token)
    album_id = context.album_ids[album]['id']
    url = '3/album/' + album_id
    get_request(context, url)
    assert album == context.response.json()['data']['title']
    assert len(context.album_ids[album]['images']) == len(context.response.json()['data']['images'])
    for index, image in enumerate(context.album_ids[album]['images']):
        assert image == context.response.json()['data']['images'][index]['id']
    if 'not' in flag:
        assert not context.response.json()['data']['favorite']
    else:
        assert context.response.json()['data']['favorite']


@when('I delete the {album} album')
def step_impl(context, album):
    set_auth_header(context, context.access_token)
    album_id = context.album_ids[album]['id']
    url = '3/album/' + album_id
    delete_request(context, url)


@then('I should not see {album} album')
def step_impl(context, album):
    set_auth_header(context, 'Client-ID ' + context.client_id)
    album_id = context.album_ids[album]['id']
    url = '3/album/' + album_id
    get_request(context, url, 404)
