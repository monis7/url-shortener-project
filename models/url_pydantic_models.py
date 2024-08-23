from pydantic import BaseModel
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from datetime import datetime

class URLMapping(Model):
    class Meta:
        table_name = "URLMapping"
        region = "us-west-2"  # Specify your AWS region

    short_url = UnicodeAttribute(hash_key=True)
    original_url = UnicodeAttribute()
    timestamp = UTCDateTimeAttribute(default=datetime.utcnow)

# Pydantic models for request and response
class URLRequest(BaseModel):
    url: str
    short_url: str = None

class URLResponse(BaseModel):
    short_url: str
    original_url: str
    timestamp: str
