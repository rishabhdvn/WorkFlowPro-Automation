import pytest
import json
import os
from playwright.sync_api import sync_playwright, Page, BrowserContext
from typing import Generator, Dict, Any

# Load test data once per session
@pytest.fixture(scope="session")
def test_data() -> Dict[str, Any]:
    # Resolves path relative to this file
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_data.json')
    with open(data_path) as f:
        return json.load(f)

# Fixture for mobile emulation (iPhone 12)
@pytest.fixture(scope="function")
def mobile_context(playwright) -> Generator[BrowserContext, None, None]:
    iphone_12 = playwright.devices['iPhone 12']
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(**iphone_12)
    yield context
    browser.close()

# Fixture to auto-inject test data into every test function
@pytest.fixture(scope="function")
def config(test_data):
    return test_data