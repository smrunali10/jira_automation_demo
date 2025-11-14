from playwright.sync_api import sync_playwright, expect
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

class JiraUI:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    @keyword("Start Browser Session")
    def start_browser_session(self, headless=False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    @keyword("Login To Jira")
    def login_to_jira(self, email, password):
        BuiltIn().log("Opening Jira login page...", level="INFO")
        self.page.goto("https://id.atlassian.com/login", timeout=60000)

        # Step 1: enter username
        self.page.get_by_test_id("username").fill(email)
        self.page.get_by_test_id("login-submit-idf-testid").click()

        # Step 2: enter password
        self.page.wait_for_selector('[data-testid="password"]', timeout=15000)
        self.page.get_by_test_id("password").fill(password)
        self.page.get_by_test_id("login-submit-idf-testid").click()

        # Step 3: wait for redirect to Atlassian home
        self.page.wait_for_selector('[data-testid="home-header-content"]', timeout=30000)

    @keyword("Open Jira Project Board")
    def open_jira_project_board(self, project_key="KAN"):
        url = f"https://smrunali46.atlassian.net/jira/software/projects/{project_key}/boards/1"
        self.page.goto(url)
        self.page.get_by_test_id("horizontal-nav.ui.content.horizontal-nav").get_by_role("link", name="List").click()

    @keyword("Validate Epic Visible By Key")
    def validate_epic_visible_by_key(self, epic_key):
        """Validate that a specific Epic issue key is visible in the board list."""
        locator = f'//a[@data-testid="native-issue-table.common.ui.issue-cells.issue-key.issue-key-cell" and text()="{epic_key}"]'
        self.page.wait_for_selector(locator, timeout=15000)
        expect(self.page.locator(locator)).to_be_visible()

    @keyword("Close Browser Session")
    def close_browser_session(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    @keyword("Update Epic Description")
    def update_epic_description(self, description_text):
        """Update the Epic description field with given text."""
        # Click description field
        self.page.get_by_test_id("issue.views.issue-base.common.description.label").click()
        self.page.get_by_role("textbox", name="Description area, start").fill(description_text)
        # Save
        self.page.get_by_test_id("comment-save-button").click()
        # Verify
        expect(self.page.get_by_text(description_text)).to_be_visible()


# from playwright.sync_api import sync_playwright, expect
# from robot.api.deco import keyword
#
# class JiraUI:
#     def __init__(self):
#         self.playwright = None
#         self.browser = None
#         self.context = None
#         self.page = None
#
#     @keyword("Start Browser Session")
#     def start_browser_session(self, headless=False):
#         self.playwright = sync_playwright().start()
#         self.browser = self.playwright.chromium.launch(headless=headless)
#         self.context = self.browser.new_context()
#         self.page = self.context.new_page()
#
#     @keyword("Login To Jira")
#     def login_to_jira(self, email, password):
#         # Go to Atlassian login
#         self.page.goto("https://id.atlassian.com/login", timeout=60000)
#
#         # Step 1: enter username
#         self.page.get_by_test_id("username").fill(email)
#         self.page.get_by_test_id("login-submit-idf-testid").click()
#
#         # Step 2: enter password
#         self.page.wait_for_selector('[data-testid="password"]', timeout=15000)
#         self.page.get_by_test_id("password").fill(password)
#         self.page.get_by_test_id("login-submit-idf-testid").click()
#
#         # ✅ Instead of waiting for Atlassian home, go directly to Jira board
#         self.page.goto(f"https://smrunali46.atlassian.net/jira/software/projects/{'KAN'}/boards/1")
#         self.page.wait_for_selector('[data-testid="horizontal-nav.ui.content.horizontal-nav"]', timeout=30000)
#
#     @keyword("Open Jira Project Board")
#     def open_jira_project_board(self, project_key="KAN"):
#         url = f"https://smrunali46.atlassian.net/jira/software/projects/{project_key}/boards/1"
#         self.page.goto(url)
#         self.page.get_by_test_id("horizontal-nav.ui.content.horizontal-nav").get_by_role("link", name="List").click()
#
#     @keyword("Validate Epic Visible By Key")
#     def validate_epic_visible_by_key(self, epic_key: str):
#         locator = f'//a[@data-testid="native-issue-table.common.ui.issue-cells.issue-key.issue-key-cell" and text()="{epic_key}"]'
#         self.page.wait_for_selector(locator, timeout=15000)
#         expect(self.page.locator(locator)).to_be_visible()
#
#     @keyword("Open Epic By Key")
#     def open_epic_by_key(self, epic_key: str):
#         locator = f'//a[@data-testid="native-issue-table.common.ui.issue-cells.issue-key.issue-key-cell" and text()="{epic_key}"]'
#         self.page.wait_for_selector(locator, timeout=15000)
#         expect(self.page.locator(locator)).to_be_visible()
#         self.page.locator(locator).click()
#         expect(self.page.get_by_test_id("issue.views.issue-base.foundation.summary.heading")).to_be_visible()
#
#     @keyword("Update Epic Description")
#     def update_epic_description(self, description_text: str):
#         # Expand description section if collapsed
#         if self.page.get_by_test_id("issue.views.common.collapsible-section.DESCRIPTION.toggle").is_visible():
#             self.page.get_by_test_id("issue.views.common.collapsible-section.DESCRIPTION.toggle").click()
#
#         # Click into description field
#         self.page.get_by_text("Description", exact=True).click()
#
#         # Fill description editor
#         editor = self.page.get_by_role("textbox", name="Description area, start")
#         editor.fill(description_text)
#
#         # Save
#         self.page.get_by_test_id("comment-save-button").click()
#
#         # Verify
#         expect(self.page.get_by_text(description_text)).to_be_visible()
#
#     @keyword("Close Browser Session")
#     def close_browser_session(self):
#         self.context.close()
#         self.browser.close()
#         self.playwright.stop()
