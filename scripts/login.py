import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.auth import get_credentials
from core.config import logger

def main():
    logger.info("Starting login / token refresh process...")
    try:
        # get_credentials handles reading token.json, checking expiry, and doing the OAuth flow if needed.
        creds = get_credentials()
        if creds and creds.valid:
            logger.info("Authentication successful. Valid token is ready for use.")
        else:
            logger.error("Authentication failed to produce a valid token.")
    except Exception as e:
        logger.error(f"Login failed: {e}")

if __name__ == "__main__":
    main()