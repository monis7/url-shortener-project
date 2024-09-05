# main.py

from fastapi import FastAPI
from api.routes import router as api_router

app = FastAPI()

# Include the API router
app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the URL Shortener API"}
