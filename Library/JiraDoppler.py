from robot.api.deco import keyword
import os, json, subprocess
from dotenv import load_dotenv
from robot.libraries.BuiltIn import BuiltIn

class JiraDoppler:

    @keyword("INITIALIZE SECRETS")
    def initialize_secrets(self):
        load_dotenv()
        token = os.getenv("DOPPLER_TOKEN")
        if not token:
            raise ValueError("DOPPLER_TOKEN is not set")

        result = subprocess.run([
            "curl", "-s",
            "-H", f"Authorization: Bearer {token}",
            "https://api.doppler.com/v3/configs/config/secrets/download?format=json"
        ], capture_output=True, text=True)

        if result.returncode != 0 or not result.stdout:
            raise RuntimeError("Failed to fetch secrets from Doppler")

        secrets = json.loads(result.stdout)
        username = secrets.get("USERNAME", "").strip()
        password = secrets.get("PASSWORD", "").strip()

        if not username or not password:
            raise ValueError("USERNAME or PASSWORD not found in Doppler secrets")

        BuiltIn().set_global_variable("${EMAIL}", username)
        BuiltIn().set_global_variable("${PASSWORD}", password)
        BuiltIn().log("INITIALIZE SECRETS executed", level="INFO")