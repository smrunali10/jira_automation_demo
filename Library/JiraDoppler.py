from robot.api.deco import keyword, library
import os, json, subprocess
from dotenv import load_dotenv
from robot.libraries.BuiltIn import BuiltIn

@library
class JiraDoppler:

    @keyword("INITIALIZE SECRETS")
    def initialize_secrets(self):
        load_dotenv()  # Load DOPPLER_TOKEN from .env
        token = os.getenv("DOPPLER_TOKEN")
        if not token:
            raise ValueError("DOPPLER_TOKEN is not set")

        # Fetch secrets from Doppler
        result = subprocess.run([
            "curl", "-s",
            "-H", f"Authorization: Bearer {token}",
            "https://api.doppler.com/v3/configs/config/secrets/download?project=jira_project&config=dev&format=json"
        ], capture_output=True, text=True)

        if result.returncode != 0 or not result.stdout:
            raise RuntimeError("Failed to fetch secrets from Doppler")

        secrets = json.loads(result.stdout)

        email = secrets.get("EMAIL", "").strip()
        ui_password = secrets.get("UI_PASSWORD", "").strip()
        api_token = secrets.get("API_TOKEN", "").strip()

        if not email or not ui_password or not api_token:
            raise ValueError("EMAIL, UI_PASSWORD, or API_TOKEN not found in Doppler secrets")

        # Set as environment variables
        os.environ["EMAIL"] = email
        os.environ["API_TOKEN"] = api_token
        os.environ["UI_PASSWORD"] = ui_password

        # Set as Robot variables
        BuiltIn().set_global_variable("${EMAIL}", email)
        BuiltIn().set_global_variable("${API_TOKEN}", api_token)
        BuiltIn().set_global_variable("${UI_PASSWORD}", ui_password)
