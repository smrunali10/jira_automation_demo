import os
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Launch browser (non-headless so you can log in)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Go to Jira login page
        page.goto("https://smrunali46.atlassian.net")

        print("👉 Please log in to Jira in the opened browser window.")
        print("   Complete 2FA if required, then wait until you see your Jira dashboard.")
        input("Press Enter here once login is complete...")

        # Save full storage state (cookies + localStorage + sessionStorage)
        save_path = os.path.join(os.path.dirname(__file__), "jira_storage.json")
        context.storage_state(path=save_path)

        print(f"✅ Jira storage state saved to: {save_path}")

        browser.close()

if __name__ == "__main__":
    main()
#========================================================================
