from robot.api.deco import keyword, library
import os, json, subprocess
from dotenv import load_dotenv
from robot.libraries.BuiltIn import BuiltIn

@library
class JiraDoppler:

    @keyword("INITIALIZE SECRETS")
    def initialize_secrets(self):
        # Load .env file (contains DOPPLER_TOKEN)
        load_dotenv()
        token = os.getenv("DOPPLER_TOKEN")
        if not token:
            raise ValueError("DOPPLER_TOKEN is not set")

        # Call Doppler API with flat JSON format
        result = subprocess.run([
            "curl", "-s",
            "-H", f"Authorization: Bearer {token}",
            "https://api.doppler.com/v3/configs/config/secrets/download?project=jira_project&config=dev&format=json"
        ], capture_output=True, text=True)

        if result.returncode != 0 or not result.stdout:
            raise RuntimeError("Failed to fetch secrets from Doppler")

        secrets = json.loads(result.stdout)

        # Extract Jira secrets directly
        email = secrets.get("EMAIL", "").strip()
        password = secrets.get("PASSWORD", "").strip()
        api_token = secrets.get("API_TOKEN", "").strip()

        if not email or not password or not api_token:
            raise ValueError("EMAIL, PASSWORD, or API_TOKEN not found in Doppler secrets")

        # Masked values for logging only
        masked_email = email[:3] + "..." + email.split("@")[-1]
        masked_token = api_token[:6] + "..." + api_token[-6:]
        masked_password = password[:3] + "..." + password[-3:]

        BuiltIn().log(f"EMAIL set to: {masked_email}", level="INFO")
        BuiltIn().log(f"API_TOKEN set to: {masked_token}", level="INFO")
        BuiltIn().log(f"PASSWORD set to: {masked_password}", level="INFO")

        # Set as environment variables for Python libraries like Playwright
        os.environ["EMAIL"] = email
        os.environ["API_TOKEN"] = api_token
        os.environ["PASSWORD"] = password

        # Also set for use inside Robot Framework directly
        BuiltIn().set_global_variable("${EMAIL}", email)
        BuiltIn().set_global_variable("${API_TOKEN}", api_token)
        BuiltIn().set_global_variable("${PASSWORD}", password)

        # Masked info only
        BuiltIn().log("EMAIL set to: *****")
        BuiltIn().log("API_TOKEN set to: *****")
        BuiltIn().log("PASSWORD set to: *****")
