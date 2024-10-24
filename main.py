# import os

import uvicorn
from fastapi import FastAPI, HTTPException

from config import supabase_client

app = FastAPI()


# Root route
@app.get("/")
async def root():
    return {"message": "Hello, World"}


# Fetch all rows from a table
@app.get("/items/")
async def get_items():
    try:
        response = supabase_client.table("user_response").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {e}")


# Insert a new row into a table
@app.post("/items/")
async def create_item(item: dict):
    try:
        response = supabase_client.table("user_response").insert(item).execute()
        return {"message": "Item created successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating item: {e}")


@app.get("/stat/")
async def get_stat():
    try:
        response = supabase_client.table("current_stat").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {e}")


@app.post("/stat/")
async def add_stat(item: dict):
    try:
        response = supabase_client.table("current_stat").insert(item).execute()
        return {"message": "Item created successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating item: {e}")


if __name__ == "__main__":
    uvicorn.run(app=app)
