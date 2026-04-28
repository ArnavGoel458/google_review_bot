import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.api import GoogleBusinessClient
from core.config import logger

def main():
    try:
        client = GoogleBusinessClient()
        logger.info("Fetching reviews...")
        
        data = client.get_reviews()
        reviews = data.get('reviews', [])
        
        logger.info(f"Successfully found {len(reviews)} reviews.\n")
        
        for review in reviews:
            name = review.get('reviewer', {}).get('displayName', 'Valued Patient')
            rating = review.get('starRating')
            comment = review.get('comment', '(No text)')
            
            print(f"[{rating}] {name}: {comment}")
            print("-" * 30)
            
    except Exception as e:
        logger.error(f"An error occurred while getting reviews: {e}")

if __name__ == "__main__":
    main()