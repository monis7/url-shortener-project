# api/routes.py

import logging
from fastapi import APIRouter, HTTPException
from models.url_pydantic_models import URLRequest, URLResponse
from api.dependencies import add_url_mapping, get_url_mapping, list_url_mappings
from service.utils import is_valid_url

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/shorten_url", response_model=URLResponse)
async def create_short_url(request: URLRequest):
    """Create a short URL for the given original URL."""
    if not is_valid_url(request.url):
        logger.error("Invalid URL format received")
        raise HTTPException(status_code=400, detail="Invalid URL format.")
    
    short_url = add_url_mapping(request.url, request.short_url)
    logger.info(f"Created short URL: {short_url} for {request.url}")
    return URLResponse(short_url=short_url, original_url=request.url, timestamp="timestamp")

@router.get("/list_urls", response_model=list[URLResponse])
async def list_urls():
    """List all short URLs and their corresponding original URLs."""
    urls = list_url_mappings()
    logger.info(f"Listing {len(urls)} URL mappings")
    return [URLResponse(short_url=item.short_url, original_url=item.original_url, timestamp=str(item.timestamp)) for item in urls]

@router.get("/redirect/{short_url}")
async def redirect(short_url: str):
    """Redirect to the original URL for the given short URL."""
    url_mapping = get_url_mapping(short_url)
    if not url_mapping:
        logger.warning(f"Attempted to redirect using non-existent short_url: {short_url}")
        raise HTTPException(status_code=404, detail=f"No URL found for '{short_url}'.")
    logger.info(f"Redirecting to original URL: {url_mapping.original_url} for short_url: {short_url}")
    return {"original_url": url_mapping.original_url}
