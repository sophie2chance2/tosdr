from playwright.sync_api import sync_playwright
import os
import requests

def create_session():
    url = "https://www.browserbase.com/v1/sessions"

    payload = {
        "projectId": os.environ["BROWSERBASE_PROJECT_ID"],
        "keepAlive": True,
        "browserSettings": {
            "context": {
                "id": os.environ["BROWSERBASE_CONTEXT_KEY"],
                "persist": True
            },
        }
    }
    headers = {
        "X-BB-API-Key": os.environ["BROWSERBASE_API_KEY"],
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()

def create_debug_url(session_id):
    url = f"https://www.browserbase.com/v1/sessions/{session_id}/debug"

    headers = {"X-BB-API-Key": os.environ["BROWSERBASE_API_KEY"]}

    response = requests.request("GET", url, headers=headers)
    debug_url = response.json()['debuggerFullscreenUrl']

    print(debug_url)

def create_context():
    url = "https://www.browserbase.com/v1/contexts"

    payload = {"projectId": os.environ["BROWSERBASE_PROJECT_ID"]}
    headers = {
        "X-BB-API-Key": os.environ["BROWSERBASE_API_KEY"],
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)

def connect_to_browser(session_id, service_id):
    with sync_playwright() as playwright:

        browser = playwright.chromium.connect_over_cdp(
            f'wss://connect.browserbase.com?apiKey={os.environ["BROWSERBASE_API_KEY"]}&sessionId={session_id}'
        )

        # Get the first page (if it exists) or create a new one
        if len(browser.contexts[0].pages) > 0:
            page = browser.contexts[0].pages[0]
        else:
            page = browser.new_page()

        page.goto(f"https://edit.tosdr.org/services/{service_id}/annotate")

        # get the dom from the page
        page_content = page.content()

        return page_content, browser