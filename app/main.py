
from fastapi import FastAPI

app = FastAPI(
    title="Virtual Closet API",
    description="Backend API untuk Virtual Closet",
    version="1.0.0",
)


@app.get("/", tags=["General"])
def home() -> dict[str, str]:
    return {"message": "Virtual Closet API is running"}


@app.get("/health", tags=["General"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
