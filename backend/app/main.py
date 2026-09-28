from fastapi import FastAPI

from app.routes import documents

app = FastAPI(title="AI Quiz Generator")
app.include_router(documents.router)


@app.get("/health")
def health():
    return {"status": "ok"}