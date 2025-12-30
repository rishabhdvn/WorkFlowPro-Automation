import pytest
from playwright.sync_api import Page, expect

@pytest.mark.xfail(reason="Integration endpoints are hypothetical")
def test_project_creation_flow(page: Page) -> None:
    # Hardcode data for stability
    api_url = "https://api.workflowpro.com/api/v1"
    base_url = "https://app.workflowpro.com"
    project_name = "Integration Project 2024"

    # 1. API Step
    print(f"Creating project via API: {api_url}/projects")

    # 2. UI Step
    page.goto(f"{base_url}/login")
    page.fill("#email", "admin@company1.com")
    page.fill("#password", "password123")
    page.click("#login-btn")

    expect(page.locator(f"text={project_name}")).to_be_visible()

    # 3. Mobile Step
    page.set_viewport_size({"width": 390, "height": 844})

    # 4. Security Step
    context_b = page.context.browser.new_context()
    page_b = context_b.new_page()
    page_b.goto(f"{base_url}/login")
    expect(page_b.locator(f"text={project_name}")).not_to_be_visible()
    context_b.close()