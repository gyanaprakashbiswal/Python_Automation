import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

# Ensure directories exist
for directory in [DATA_DIR, LOGS_DIR, SCREENSHOTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configuration from environment
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEFAULT_SCRAPE_URL = os.getenv("DEFAULT_SCRAPE_URL", "https://example.com")
TARGET_LOGIN_URL = os.getenv("TARGET_LOGIN_URL", "https://the-internet.herokuapp.com/login")
TEST_USERNAME = os.getenv("TEST_USERNAME", "tomsmith")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "SuperSecretPassword!")
