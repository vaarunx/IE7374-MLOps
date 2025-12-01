from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

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

# GET /albums - Get all albums
@app.get("/albums", response_model=List[Album])
async def get_albums():
    """Get all albums"""
    return albums

# POST /albums - Create a new album
@app.post("/albums", response_model=Album, status_code=201)
async def post_albums(album: Album):
    """Add a new album"""
    albums.append(album)
    return album

# GET /albums/{id} - Get album by ID
@app.get("/albums/{id}", response_model=Album)
async def get_album_by_id(id: str):
    """Get a specific album by ID"""
    for album in albums:
        if album.id == id:
            return album
    raise HTTPException(status_code=404, detail="album not found")

# PUT /albums/{id} - Update an existing album
@app.put("/albums/{id}", response_model=Album)
async def update_existing_album(id: str, updated_album: AlbumUpdate):
    """Update an existing album"""
    for i, album in enumerate(albums):
        if album.id == id:
            # Update the album fields
            albums[i].title = updated_album.title
            albums[i].artist = updated_album.artist
            albums[i].price = updated_album.price
            return albums[i]
    
    raise HTTPException(status_code=404, detail="album not found")

# DELETE /albums/{id} - Delete an album
@app.delete("/albums/{id}")
async def delete_album(id: str):
    """Delete an album by ID"""
    for i, album in enumerate(albums):
        if album.id == id:
            albums.pop(i)
            return {"message": "album deleted successfully"}
    
    raise HTTPException(status_code=404, detail="album not found")

def print_this():
    if albums:
        print(albums[0].id)

# Main entry point
if __name__ == "__main__":
    print_this()
    uvicorn.run(app, host="0.0.0.0", port=8080)