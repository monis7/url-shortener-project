from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.url_pydantic_models import URLRequest, URLResponse
from service.url_service import add_url_mapping, get_original_url, list_all_urls
from service.utils import is_valid_url
from api.dependencies import add_url_mapping, get_url_mapping, list_url_mappings


router = APIRouter()

# Define your API routes here


@router.get("/")
async def read_root():
    return {"message": "Welcome to the URL Shortener API"}

@router.post("/shorten_url", response_model=URLResponse)
async def create_short_url(request: URLRequest):
    """Create a short URL for the given original URL."""
    if not is_valid_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL format.")

    short_url = add_url_mapping(request.url, request.short_url)
    return URLResponse(short_url=short_url, original_url=request.url, timestamp="timestamp")

@router.get("/list_urls", response_model=list[URLResponse])
async def list_urls():
    """List all short URLs and their corresponding original URLs."""
    urls = list_url_mappings()
    return [URLResponse(short_url=item.short_url, original_url=item.original_url, timestamp=str(item.timestamp)) for item in urls]

@router.get("/redirect/{short_url}")
async def redirect(short_url: str):
    """Redirect to the original URL for the given short URL."""
    url_mapping = get_url_mapping(short_url)
    if not url_mapping:
        raise HTTPException(status_code=404, detail=f"No URL found for '{short_url}'.")
    return {"original_url": url_mapping.original_url}