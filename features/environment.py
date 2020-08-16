from behave import fixture, use_fixture
from splinter import Browser
import os
import shutil
import time
from purl import URL


@fixture
def browser_chrome(context):
    # -- SETUP-FIXTURE PART:
    context.browser = Browser('chrome', headless=headless(context))
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.quit()


@fixture
def browser_firefox(context):
    # -- SETUP-FIXTURE PART:
    context.browser = Browser(headless=headless(context))
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.quit()


def before_feature(context, feature):
    context.config.show_skipped = False
    if "skip" in feature.tags:
        feature.skip("Marked with @skip")
        return


def clean_state(context):
    try:
        context.browser.driver.delete_all_cookies()
        context.browser.driver.execute_script('window.localStorage.clear();')
        context.browser.visit('about:blank')
    except Exception:
        pass


def before_scenario(context, scenario):
    context.config.show_skipped = False
    if "skip" in scenario.tags:
        scenario.skip("Marked with @skip")
        return

    # Default repeat attempt counts and delay for polling GET.
    context.n_attempts = 10
    context.pause_between_attempts = 0.05

    # Do not authenticate by default.
    context.auth = None

    # Verify server certificate by default.
    context.verify_ssl = False
    context.uploaded_images = {}
    context.album_ids = {}


def headless(context):
    return context.config.userdata.getbool('HEADLESS', True)


def set_api_params(context):
    context.headers = {}
    context.api_url = 'https://api.imgur.com'
    context.server = URL(context.api_url)
    context.headers['Accept'.encode('ascii')] = 'application/json'.encode('ascii')
    context.headers['Content-Type'.encode('ascii')] = 'application/json'.encode('ascii')
    context.template_data = {}


def before_all(context):
    set_api_params(context)

    context.config.show_skipped = False
    os.system('rm failed_scenarios_screenshots/*.png')
    if 'BROWSER' in context.config.userdata.keys():
        if context.config.userdata['BROWSER'] is None:
            BROWSER = 'chrome'
        else:
            BROWSER = context.config.userdata['BROWSER']
        if BROWSER == 'chrome':
            use_fixture(browser_chrome, context)
        elif BROWSER == 'firefox':
            use_fixture(browser_firefox, context)
        else:
            print('Browser you entered:', BROWSER, 'is invalid value')


def after_scenario(context, scenario):
    if scenario.status == 'failed ' and 'BROWSER' in context.config.userdata.keys():
        name = 'failed_scenarios_screenshots/' + '_'.join(map(str, scenario.name.lower().split(' '))) + '.png'
        context.browser.driver.save_screenshot(name)
        logs = []
        for log in context.browser.driver.get_log('browser'):
            if "Warning: " not in log['message'] and log['level'] != 'WARNING':
                logs.append(log)
        if logs:
            print('*********************Console Logs\n')
            print(logs)
        clean_state(context)


def after_all(context):
    if 'ARCHIVE' in context.config.userdata.keys():
        if context.config.userdata['ARCHIVE'] == 'Yes':
            shutil.make_archive(
                time.strftime('%d_%m_%Y_%H_%M_%S'),
                'zip',
                'failed_scenarios_screenshots')
