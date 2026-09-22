from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

nuevo_usuario = {
    "Name": "Marcos",
    "Weight": 75,
    "Height": 178,
    "Objective": "ganar masa muscular",
    "Activity": "5"
}


resultado = supabase.table("USERS").insert(nuevo_usuario).execute()

print("Usuario insertado:", resultado.data)