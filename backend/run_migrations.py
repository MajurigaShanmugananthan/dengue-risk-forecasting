import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from app.models import Base

def migrate():
    load_dotenv()  # ✅ Load .env
    database_url = os.getenv("DATABASE_URL")
    print("Using DB:", database_url)  # ✅ Debug check
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created!")

if __name__ == "__main__":
    migrate()
