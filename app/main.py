from fastapi import FastAPI, HTTPException
from app.routers import books

app = FastAPI()

app.include_router(books.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "library-management-api"}