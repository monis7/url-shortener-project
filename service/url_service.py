import uuid
import random
import string
# This is where your URL shortening logic will go
def generate_short_url(url: str, short_id_length: int) -> str:
     # Generate a UUID and take the first `short_id_length` characters for a short URL
    short_url = str(uuid.uuid4()).replace('-', '')[:short_id_length]
    return short_url
