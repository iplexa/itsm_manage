from fastapi import FastAPI

from app.api.routes import batches, config, import_, tasks
from app.core.logging import configure_logging


configure_logging()

app = FastAPI(title="ITSM Manage API")
app.include_router(batches.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(import_.router, prefix="/api")
app.include_router(config.router, prefix="/api")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
