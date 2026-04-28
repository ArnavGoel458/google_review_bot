import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from config import CREDENTIALS_FILE, SCOPES, logger

def get_credentials() -> Credentials:
    """
    Retrieves or generates OAuth2 credentials.
    It checks for an existing `token.json`, refreshes it if expired, 
    or starts the local server flow to log the user in.
    """
    creds = None
    
    # 1. Check if we already have a saved token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        logger.info("Found existing token.json.")

    # 2. If there are no valid credentials (first time or expired), log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Token expired. Refreshing automatically...")
            try:
                creds.refresh(Request())
            except Exception as e:
                logger.error(f"Failed to refresh token: {e}")
                creds = None
                
        if not creds:
            logger.info("No valid token found. Opening browser for initial login...")
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"OAuth credentials file '{CREDENTIALS_FILE}' not found.")
            
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # 3. Save the credentials (including the Refresh Token) for next time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            logger.info("Success! token.json has been created/updated.")

    return creds

def get_authorized_token() -> str:
    """Helper to quickly get just the token string, ensuring it's valid."""
    creds = get_credentials()
    return creds.token
