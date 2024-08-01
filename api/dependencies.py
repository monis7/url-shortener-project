# Add your dependency injections and helper functions here
# api/dependencies.py

from typing import Optional
from pynamodb.exceptions import DoesNotExist
from models.url_pynamodb_models import URLMapping

def get_url_mapping(short_url: str) -> Optional[URLMapping]:
    """Retrieve the URL mapping from DynamoDB."""
    try:
        url_mapping = URLMapping.get(short_url)
        return url_mapping
    except DoesNotExist:
        return None

def add_url_mapping(original_url: str, short_url: Optional[str] = None) -> str:
    """Add a new URL mapping to DynamoDB and return the short URL."""
    if not short_url:
        short_url = generate_unique_short_url()
    
    url_mapping = URLMapping(short_url=short_url, original_url=original_url)
    url_mapping.save()
    return short_url

def list_url_mappings() -> list:
    """Retrieve all URL mappings from DynamoDB."""
    return list(URLMapping.scan())

def generate_unique_short_url(length: int = 6) -> str:
    """Generate a unique short URL."""
    from service.url_service import generate_short_url

    short_url = generate_short_url(length)
    # Ensure uniqueness by checking if it already exists
    while get_url_mapping(short_url):
        short_url = generate_short_url(length)
    return short_url
