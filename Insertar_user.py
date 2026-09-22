from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

usuario = {
    "email": "marcosportillop03@gmail.com",
    "Name": "Marcos",
    "Weight": 88,
    "Height": 181,
    "Objective": "ganar masa muscular",
    "Activity": 5
}

resultado = supabase.table("USERS").upsert(usuario, on_conflict="email").execute()

print("Usuario actualizado/insertado:", resultado.data)