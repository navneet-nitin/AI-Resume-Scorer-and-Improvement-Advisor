from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.api.health import router as health_router

app = FastAPI(
    title="AI Resume Scorer API",
    version="1.0.0"
)

# CORS (important for frontend later)
origins = [
    "http://localhost:3000",
    "http://localhost:5500",  # VS Code Live Server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(api_router, prefix="/api")
app.include_router(health_router)


@app.get("/")
def root():
    return {"message": "Resume Scorer API is running 🚀"}