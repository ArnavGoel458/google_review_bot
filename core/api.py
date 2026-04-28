import requests
from googleapiclient.discovery import build
from .auth import get_credentials, get_authorized_token
from .config import ACCOUNT_ID, LOCATION_ID, logger

class GoogleBusinessClient:
    """
    Wrapper for Google My Business APIs.
    We use `googleapiclient` for business info and raw `requests` for the Business Profile APIs 
    where required by the current integration.
    """
    def __init__(self):
        self.creds = get_credentials()
        self.access_token = get_authorized_token()
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def get_accounts_and_locations(self):
        """Fetches the account ID and locations using the python client library."""
        try:
            account_mgmt = build('mybusinessaccountmanagement', 'v1', credentials=self.creds, cache_discovery=False)
            accounts = account_mgmt.accounts().list().execute()
            
            if not accounts.get('accounts'):
                logger.warning("No accounts found. Make sure you are the owner of the profile.")
                return None, None

            account_name = accounts['accounts'][0]['name']
            
            # Mask the account ID for safe logging
            acc_id = account_name.rsplit('/', 1)[-1]
            masked_acc = f"accounts/****{acc_id[-4:]}" if len(acc_id) > 4 else "accounts/****"
            logger.info(f"Found Account: {masked_acc}")

            biz_info = build('mybusinessbusinessinformation', 'v1', credentials=self.creds, cache_discovery=False)
            locations = biz_info.accounts().locations().list(
                parent=account_name, readMask="name,title"
            ).execute()

            loc_list = locations.get('locations', [])
            for loc in loc_list:
                # Mask the location ID for safe logging
                loc_id = loc['name'].rsplit('/', 1)[-1]
                masked_loc = f"locations/****{loc_id[-4:]}" if len(loc_id) > 4 else "locations/****"
                logger.info(f" -> Location: {loc['title']} (ID: {masked_loc})")
                
            return account_name, loc_list

        except Exception as e:
            logger.error(f"Failed to fetch accounts/locations: {e}")
            return None, None

    def get_reviews(self, page_token=None):
        """Fetches a list of reviews for the configured location."""
        if not ACCOUNT_ID or not LOCATION_ID:
            raise ValueError("ACCOUNT_ID or LOCATION_ID is missing from environment/config.")

        url = f"https://mybusiness.googleapis.com/v4/accounts/{ACCOUNT_ID}/locations/{LOCATION_ID}/reviews"
        if page_token:
            url += f"?pageToken={page_token}"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to fetch reviews: {response.status_code} - {response.text}")
            return {}

    def post_reply(self, review_name: str, message: str) -> bool:
        """Posts a reply to a specific review."""
        url = f"https://mybusiness.googleapis.com/v4/{review_name}/reply"
        payload = {"comment": message}
        
        response = requests.put(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            return True
        else:
            logger.error(f"Failed to reply to {review_name}: {response.status_code} - {response.text}")
            return False
