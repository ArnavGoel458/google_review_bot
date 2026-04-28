import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from core.api import GoogleBusinessClient
from core.config import logger, get_reply_template

def main():
    try:
        client = GoogleBusinessClient()
        template = get_reply_template()
        
        next_page_token = None
        total_processed = 0

        logger.info("--- Starting Full Review Scan ---")

        while True:
            data = client.get_reviews(page_token=next_page_token)
            if not data:
                logger.error("No data received or API error.")
                break

            reviews = data.get('reviews', [])
            
            for review in reviews:
                name = review.get('reviewer', {}).get('displayName', 'Valued Patient')
                rating = review.get('starRating')
                review_path = review.get('name')
                already_replied = 'reviewReply' in review

                if rating in ["FOUR", "FIVE"] and not already_replied:
                    logger.info(f"[{rating}] Replying to {name}...")
                    
                    # Format the reply message template with the reviewer's name
                    message = template.format(reviewer_name=name)
                    
                    success = client.post_reply(review_path, message)
                    if success:
                        logger.info(f"   ✅ Replied to {name}.")
                        # Safety delay to stay under API rate limits
                        time.sleep(1) 
                    else:
                        logger.error(f"   ❌ Failed to reply to {name}.")
                
                total_processed += 1

            next_page_token = data.get('nextPageToken')
            if not next_page_token:
                logger.info("No more pages left.")
                break
            
            logger.info(f"--- Fetched {total_processed} reviews so far. Moving to next page... ---")

        logger.info(f"--- Task Complete. Total reviews scanned: {total_processed} ---")

    except Exception as e:
        logger.error(f"An error occurred during review scanning: {e}")

if __name__ == "__main__":
    main()