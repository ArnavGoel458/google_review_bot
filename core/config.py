import os
import logging
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants and Environment Variables
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
LOCATION_ID = os.getenv('LOCATION_ID')
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE', 'credentials.json')

SCOPES = ['https://www.googleapis.com/auth/business.manage']

# Load templates
TEMPLATE_FILE = 'templates.yaml'

def get_reply_template() -> str:
    """Loads the reply template from the YAML configuration."""
    try:
        if os.path.exists(TEMPLATE_FILE):
            with open(TEMPLATE_FILE, 'r') as f:
                data = yaml.safe_load(f)
                return data.get('reply_template', "")
    except Exception as e:
        logger.error(f"Error loading template from {TEMPLATE_FILE}: {e}")
    
    # Fallback default
    logger.warning("Using fallback reply template.")
    return "Thank you so much, {reviewer_name}, for your kind words! We are committed to providing top service."

