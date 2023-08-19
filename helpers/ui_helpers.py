from playwright.sync_api import sync_playwright


def initiate_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    return page
