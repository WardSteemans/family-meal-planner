import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# 1. Laad de variabelen uit het .env bestand
load_dotenv()

# 2. Haal de DATABASE_URL op
DATABASE_URL = os.getenv("DATABASE_URL")

# Veiligheidscheck: stop het programma als de URL mist
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is niet ingesteld in het .env bestand!")

# 3. Maak de engine aan
# echo=True is handig tijdens development (je ziet alle SQL queries in je terminal)
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)