from playwright.sync_api import APIRequestContext, Page
from creds import *


def test_create_issue(api_context: APIRequestContext):
    issue_data = {
        'title': '[BUG] That Went Wrong',
        'body': 'When doing this, that failed'
    }

    post_response = api_context.post(
        f'/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/issues',
        data=issue_data
    )

    assert post_response.ok


def test_take_issue_screenshot(page: Page):
    page.goto(f'https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}/issues')
    page.screenshot(path='issue-page.jpg', full_page=True)


def test_new_issue_in_repo(api_context: APIRequestContext):
    all_issues = api_context.get(
        f'/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/issues'
    )

    assert all_issues.ok

    new_issue = [issue for issue in all_issues.json() if issue['title'] == '[BUG] That Went Wrong'][0]

    assert new_issue['body'] == 'When doing this, that failed'

