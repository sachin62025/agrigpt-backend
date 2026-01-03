import uvicorn
from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="AgriGPT Backend",
    description="Agentic RAG for Citrus Farmers",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "AgriGPT API is running. "}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)