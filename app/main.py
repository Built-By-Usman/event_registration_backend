from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base
from dotenv import load_dotenv
from app.routers import auth, user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Event Registration System", root_path="/event_registration_system")
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your React URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


@app.get("/")
def index():
    return "hello"


app.include_router(auth.router)
app.include_router(user.router)
