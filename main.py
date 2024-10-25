import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import supabase_client

app = FastAPI()

# Configure CORS
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],  # Allow requests from your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Define a Pydantic model for user_response
class UserResponse(BaseModel):
    # Replace with actual fields from your database schema
    TeamID: str
    SubmittedBy: str
    UpdateType: str
    venue_id: str
    Content: dict
    # Add other fields as per your table schema


# Define a Pydantic model for current_stat
class CurrentStat(BaseModel):
    # Replace with actual fields from your database schema
    team_id: int
    msg_ids: int
    # Add other fields as per your table schema


# Root route
@app.get(path="/")
async def root():
    return {"message": "Hello, World"}


# Fetch all rows from a table : user_response database
@app.get(path="/usr_resp/all", description="Fetch all rows from a user_response table")
async def get_usr_resp():
    try:
        response = supabase_client.table("user_response").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {e}")


# Insert a new row into a table : user_response database
@app.post(
    path="/usr_resp/add", description="Insert a new row from a user_response table"
)
async def add_usr_resp(item: dict):
    try:
        response = supabase_client.table("user_response").insert(item).execute()
        return {"message": "Item created successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating item: {e}")


# Fetch all rows from a table : current_stat database
@app.get(path="/stat/all", description="Fetch all rows from a current_stat table")
async def get_stat():
    try:
        response = supabase_client.table("current_stat").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {e}")


# Insert a new row into a table : current_stat database
@app.post(path="/stat/add", description="Insert a new row from a current_stat table")
async def add_stat(item: dict):
    try:
        response = supabase_client.table("current_stat").insert(item).execute()
        return {"message": "Item created successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating item: {e}")


# Fetch rows by venue_id from the user_response table
@app.get(
    path="/venue/{venue_id}",
    description="Fetch rows by venue_id from the user_response table",
)
async def get_by_venue_id(venue_id: str):
    try:
        response = (
            supabase_client.table("user_response")
            .select("*")
            .eq("venue_id", venue_id)
            .execute()
        )
        if not response.data:
            raise HTTPException(
                status_code=404, detail="No records found for the given venue_id"
            )
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching items by venue_id: {e}"
        )


if __name__ == "__main__":
    uvicorn.run(app=app)
