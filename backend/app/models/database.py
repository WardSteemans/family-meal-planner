from sqlmodel import SQLModel, create_engine, Session

# Pas dit aan naar jouw DB URL
DATABASE_URL = "postgresql://user:password@localhost:5432/family_meal_planner"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)