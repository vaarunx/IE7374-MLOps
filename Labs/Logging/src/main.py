from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging

# Configure logging with both console and file output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('albums_api.log'),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

# Create a custom logger for the albums API
logger = logging.getLogger("albums_api")

# Album model using Pydantic for request/response validation
class Album(BaseModel):
    id: str
    title: str
    artist: str
    price: float

# Update model (for PUT requests where ID might not be in body)
class AlbumUpdate(BaseModel):
    title: str
    artist: str
    price: float

# Initialize FastAPI app
app = FastAPI(title="Albums API", version="1.0.0")

albums = [
    Album(id="1", title="Life of a Showgirl", artist="Taylor Swift", price=13.99),
    Album(id="2", title="Brat", artist="Charli XCX", price=17.99),
    Album(id="3", title="Hurry Up Tomorrow", artist="Weeknd", price=19.99),
]

logger.info("Albums API initialized with %d albums", len(albums))

# GET /albums - Get all albums
@app.get("/albums", response_model=List[Album])
async def get_albums():
    """Get all albums"""
    logger.debug("Fetching all albums from the collection")
    logger.info("GET /albums - Returning %d albums", len(albums))
    return albums

# POST /albums - Create a new album
@app.post("/albums", response_model=Album, status_code=201)
async def post_albums(album: Album):
    """Add a new album"""
    logger.debug("Attempting to add new album: %s", album.dict())
    
    # Check for duplicate ID (this will generate a WARNING)
    for existing_album in albums:
        if existing_album.id == album.id:
            logger.warning("Duplicate album ID detected: %s. Overwriting existing album.", album.id)
    
    albums.append(album)
    logger.info("POST /albums - Successfully added album: %s by %s", album.title, album.artist)
    return album

# GET /albums/{id} - Get album by ID
@app.get("/albums/{id}", response_model=Album)
async def get_album_by_id(id: str):
    """Get a specific album by ID"""
    logger.debug("Searching for album with ID: %s", id)
    
    for album in albums:
        if album.id == id:
            logger.info("GET /albums/%s - Album found: %s", id, album.title)
            return album
    
    logger.error("GET /albums/%s - Album not found", id)
    raise HTTPException(status_code=404, detail="album not found")

# PUT /albums/{id} - Update an existing album
@app.put("/albums/{id}", response_model=Album)
async def update_existing_album(id: str, updated_album: AlbumUpdate):
    """Update an existing album"""
    logger.debug("Attempting to update album with ID: %s", id)
    
    # Check for suspicious price changes
    for i, album in enumerate(albums):
        if album.id == id:
            old_price = album.price
            new_price = updated_album.price
            
            if new_price > old_price * 2:
                logger.warning("Significant price increase detected for album %s: $%.2f -> $%.2f", 
                             id, old_price, new_price)
            
            # Update the album fields
            albums[i].title = updated_album.title
            albums[i].artist = updated_album.artist
            albums[i].price = updated_album.price
            
            logger.info("PUT /albums/%s - Successfully updated album: %s", id, albums[i].title)
            return albums[i]
    
    logger.error("PUT /albums/%s - Album not found for update", id)
    raise HTTPException(status_code=404, detail="album not found")

# DELETE /albums/{id} - Delete an album
@app.delete("/albums/{id}")
async def delete_album(id: str):
    """Delete an album by ID"""
    logger.debug("Attempting to delete album with ID: %s", id)
    
    # Check if we're deleting the last album (CRITICAL situation)
    if len(albums) == 1:
        logger.critical("CRITICAL: Attempting to delete the last album in the collection!")
    
    for i, album in enumerate(albums):
        if album.id == id:
            deleted_album = albums.pop(i)
            logger.info("DELETE /albums/%s - Successfully deleted album: %s", id, deleted_album.title)
            return {"message": "album deleted successfully"}
    
    logger.error("DELETE /albums/%s - Album not found for deletion", id)
    raise HTTPException(status_code=404, detail="album not found")

def print_this():
    """Test function that demonstrates exception logging"""
    try:
        if albums:
            logger.debug("print_this() called - accessing first album")
            print(albums[0].id)
            
        # Simulate a potential error scenario
        result = 10 / 0  # This will raise ZeroDivisionError
    except ZeroDivisionError:
        logger.exception("Exception occurred in print_this() function")

# Main entry point
if __name__ == "__main__":
    logger.info("Starting Albums API server on http://0.0.0.0:8080")
    print_this()
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")