import random
from playwright.sync_api import sync_playwright


def initiate_browser():
    p = sync_playwright().start()
    user_agent_strings = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    ]
    ua = user_agent_strings[random.randint(0, len(user_agent_strings) - 1)]
    # Switched browser to firefox, because chromium does not support use of proxy server
    browser = p.firefox.launch(headless=False)
    page = browser.new_page(user_agent=ua, proxy={"server": "192.168.1.92:808"})
    return page
