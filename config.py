import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

base_url = os.getenv("supabase_url")
base_key = os.getenv("supabase_key")

supabase_client: Client = create_client(supabase_url=base_url, supabase_key=base_key)
