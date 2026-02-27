from database import engine
from models import Base
import os
print("DATABASE_URL:", os.getenv("DATABASE_URL"))
# ✅ This creates all tables defined in models.py
Base.metadata.create_all(bind=engine)