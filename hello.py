import os
from dotenv import load_dotenv
load_dotenv()

USE_NEONDB = os.getenv('USE_NEONDB')
USE_SUPABASE = os.getenv('USE_SUPABASE')

if USE_NEONDB == "True":

    NEONDB_URL = os.getenv("NEON_DB")
    # db = PostgresDb(db_url=NEONDB_URL)
    print("using neon db")
elif USE_SUPABASE == True:
#     SUPABASE_PROJECT = getenv("SUPABASE_PROJECT")
#     SUPABASE_PASSWORD = getenv("SUPABASE_PASSWORD")

#     SUPABASE_DB_URL = (
#     f"postgresql://postgres:{SUPABASE_PASSWORD}@db.{SUPABASE_PROJECT}:5432/postgres"
#     )
# # Setup the Supabase database
#     db = PostgresDb(db_url=SUPABASE_DB_URL)
    print("using supabase db")
else:
    print("NO DB USED")