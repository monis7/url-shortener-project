import random
import string
# This is where your URL shortening logic will go
def generate_short_url(url: str, short_id_length: int) -> str:
    # Implement your URL shortening logic here
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=short_id_length))
