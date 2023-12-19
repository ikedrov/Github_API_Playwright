import pytest
from playwright.sync_api import APIRequestContext, Playwright
from creds import *


@pytest.fixture(scope='session')
def api_context(playwright: Playwright):
    context = playwright.request.new_context(
        base_url='https://api.github.com',
        extra_http_headers={
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {GITHUB_ACCESS_TOKEN}'
        }
    )
    yield context
    context.dispose()


@pytest.fixture(autouse=True, scope='session')
def create_test_repo(api_context: APIRequestContext):
    post_response = api_context.post(
        '/user/repos',
        data={'name': GITHUB_REPO}
    )
    assert post_response.ok

    yield

    delete_response = api_context.delete(
        f'/repos/{GITHUB_USERNAME}/{GITHUB_REPO}'
    )
    assert delete_response.ok

    