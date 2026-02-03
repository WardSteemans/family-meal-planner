from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Family Meal Planner API")

# CORS voor React Native (later aanpassen naar je domein)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Family Meal Planner API running!"}