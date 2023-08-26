from playwright.sync_api import sync_playwright


def initiate_browser():
    p = sync_playwright().start()
    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/69.0.3497.100 Safari/537.36"
    )
    browser = p.chromium.launch(headless=False)
    page = browser.new_page(user_agent=ua)
    return page
