from api import GoogleBusinessClient
from config import logger

def main():
    logger.info("Fetching Business Information...")
    client = GoogleBusinessClient()
    account_name, locations = client.get_accounts_and_locations()
    
    if not account_name:
        logger.error("Failed to retrieve accounts. Check your credentials.")
        return
        
    acc_id = account_name.rsplit('/', 1)[-1]
    masked_acc = f"accounts/****{acc_id[-4:]}" if len(acc_id) > 4 else "accounts/****"
    logger.info(f"Successfully connected to account: {masked_acc}")
    logger.info(f"Total locations found: {len(locations)}")

if __name__ == '__main__':
    main()