# api/dependencies.py

import logging
from typing import Optional
from pynamodb.exceptions import DoesNotExist
from models.url_pynamodb_models import URLMapping
from service.url_service import ensure_unique_short_url

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_url_mapping(short_url: str) -> Optional[URLMapping]:
    """Retrieve the URL mapping from DynamoDB."""
    try:
        url_mapping = URLMapping.get(short_url)
        logger.info(f"Retrieved URL mapping for short_url: {short_url}")
        return url_mapping
    except DoesNotExist:
        logger.warning(f"No URL mapping found for short_url: {short_url}")
        return None

def add_url_mapping(original_url: str, short_url: Optional[str] = None) -> str:
    """Add a new URL mapping to DynamoDB and return the short URL."""
    if not short_url:
        # Retrieve all existing short URLs from the database
        existing_short_urls = set(item.short_url for item in URLMapping.scan())
        short_url = ensure_unique_short_url(existing_short_urls)
    
    url_mapping = URLMapping(short_url=short_url, original_url=original_url)
    url_mapping.save()
    logger.info(f"Added URL mapping: {short_url} -> {original_url}")
    return short_url

def list_url_mappings() -> list:
    """Retrieve all URL mappings from DynamoDB."""
    urls = list(URLMapping.scan())
    logger.info(f"Retrieved {len(urls)} URL mappings from DynamoDB")
    return urls
