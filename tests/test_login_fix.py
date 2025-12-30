import pytest
from playwright.sync_api import Page, expect
from typing import Dict, Any

def test_user_login_reliable(page: Page, config: Dict[str, Any]) -> None:
    """
    [Part 1 Solution] Refactored login test to fix CI/CD flakiness.
    
    Fixes applied:
    1. Replaced immediate 'assert' with auto-retrying 'expect()'.
    2. Added visibility checks for dynamic elements.
    3. Extracted hardcoded credentials to data file.
    """
    user = config['admin_user']
    base_url = config['urls']['base_url']

    # 1. Navigate
    page.goto(f"{base_url}/login")

    # 2. Interaction
    page.fill("#email", user['email'])
    page.fill("#password", user['password'])
    page.click("#login-btn")

    # 3. Validation (The Fix)
    # expect() polls the URL until timeout or success, fixing race conditions.
    expect(page).to_have_url(f"{base_url}/dashboard")
    
    # Check for element visibility to ensure page interactivity
    expect(page.locator(".welcome-message")).to_be_visible()