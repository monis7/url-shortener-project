# service/url_service.py

import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_short_url(short_id_length: int = 6) -> str:
    """
    Generate a short URL identifier using uuid.
    
    :param short_id_length: Length of the short URL identifier
    :return: A random string of letters and digits of specified length
    """
    if short_id_length <= 0:
        raise ValueError("Short ID length must be greater than 0")
    
    short_url = str(uuid.uuid4()).replace('-', '')[:short_id_length]
    logger.info(f"Generated short URL: {short_url}")
    return short_url

def ensure_unique_short_url(existing_urls: set, short_id_length: int = 6) -> str:
    """
    Generate a unique short URL identifier that does not collide with existing ones.
    
    :param existing_urls: A set of currently existing short URLs
    :param short_id_length: Length of the short URL identifier
    :return: A unique short URL
    """
    short_url = generate_short_url(short_id_length)
    while short_url in existing_urls:
        short_url = generate_short_url(short_id_length)
    logger.info(f"Ensured unique short URL: {short_url}")
    return short_url
