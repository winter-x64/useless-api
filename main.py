import uvicorn
from fastapi import FastAPI, HTTPException

from config import supabase_client

app = FastAPI()


# Root route
@app.get("/")
async def root():
    return {"message": "Hello, World"}


# Fetch all rows from a table : user_response database
@app.get("/usr_resp/all", description="Fetch all rows from a user_response table")
async def get_usr_resp():
    try:
        response = supabase_client.table("user_response").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {e}")


# Insert a new row into a table : user_response database
@app.post("/usr_resp/add", description="Insert a new row from a user_response table")
async def add_usr_resp(item: dict):
    try:
        response = supabase_client.table("user_response").insert(item).execute()
        return {"message": "Item created successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating item: {e}")


# Fetch all rows from a table : current_stat database
@app.get("/stat/all", description="Fetch all rows from a current_stat table")
async def get_stat():
    try:
        response = supabase_client.table("current_stat").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {e}")


# Insert a new row into a table : current_stat database
@app.post("/stat/add", description="Insert a new row from a current_stat table")
async def add_stat(item: dict):
    try:
        response = supabase_client.table("current_stat").insert(item).execute()
        return {"message": "Item created successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating item: {e}")


if __name__ == "__main__":
    uvicorn.run(app=app)
