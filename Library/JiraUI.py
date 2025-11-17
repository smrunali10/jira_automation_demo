import os
from robot.api.deco import keyword, library
from playwright.sync_api import sync_playwright, expect
from robot.api import logger

@library
class JiraUI:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    @keyword("Start Browser Session")
    def start_browser_session(self, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    @keyword("Login With Cookies Or Fallback")
    def login_with_cookies_or_fallback(self, email=None, password=None, storage_file="jira_storage.json"):
        storage_path = os.path.join(os.path.dirname(__file__), storage_file)
        print("Looking for storage state at:", storage_path)

        if os.path.exists(storage_path):
            try:
                self.context = self.browser.new_context(storage_state=storage_path)
                self.page = self.context.new_page()
                self.page.goto("https://smrunali46.atlassian.net", timeout=60000)
                self.page.wait_for_selector("a[href*='/browse/']", timeout=40000)
                logger.info("Logged in with storage state")
                return
            except Exception as e:
                logger.warn(f"Storage state login failed: {e}. Falling back to credentials.")

        if email and password:
            self.login_to_jira(email, password)
        else:
            raise RuntimeError("No storage state and no credentials provided")

    @keyword("Login To Jira")
    def login_to_jira(self, email, password):
        logger.info("Opening Jira login page...")
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto("https://id.atlassian.com/login", timeout=60000)
        self.page.get_by_test_id("username").fill(email)
        self.page.get_by_test_id("login-submit-idf-testid").click()
        self.page.wait_for_selector('[data-testid="password"]', timeout=15000)
        self.page.get_by_test_id("password").fill(password)
        self.page.get_by_test_id("login-submit-idf-testid").click()
        self.page.wait_for_selector("a[href*='/browse/JIRA']", timeout=60000)

    # @keyword("Open Jira Project Board")
    # def open_jira_project_board(self, project_key="JIRA"):
    #     xpath = f"//a[contains(@href,'/browse/{project_key}')]"
    #     self.page.wait_for_selector(xpath, timeout=60000)
    #     project_link = self.page.locator(xpath).first
    #     project_link.scroll_into_view_if_needed()
    #     project_link.click(force=True)
    #
    #     # elements = self.page.locator("//h2//span").all_text_contents()
    #     # print("Found spans:", elements)
    #
    #     self.page.wait_for_selector("//span[normalize-space(text())='List']", timeout=60000)
    #     self.page.locator("//span[normalize-space(text())='List']").click()
    @keyword("Open Jira Project Board")
    def open_jira_project_board(self, project_key="JIRA"):
        # Target the project board link (not browse link)
        xpath = f"//a[contains(@href,'/jira/software/projects/{project_key}/boards')]"
        self.page.wait_for_selector(xpath, timeout=60000)
        project_link = self.page.locator(xpath).first
        project_link.scroll_into_view_if_needed()
        project_link.click(force=True)

        # Wait until the board view loads
        self.page.wait_for_selector("//span[normalize-space(text())='List']", timeout=60000)
        self.page.locator("//span[normalize-space(text())='List']").click()

    @keyword("Validate Epic Visible By Key")
    def validate_epic_visible_by_key(self, epic_key):
        locator = f'//a[@data-testid="native-issue-table.common.ui.issue-cells.issue-key.issue-key-cell" and text()="{epic_key}"]'
        self.page.wait_for_selector(locator, timeout=15000)
        expect(self.page.locator(locator)).to_be_visible()

    @keyword("Close Browser Session")
    def close_browser_session(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
