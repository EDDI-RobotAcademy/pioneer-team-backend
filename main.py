from fastapi import FastAPI

from app.domains.ceo_test.adapter.inbound.api.ceo_test_router import (
    router as ceo_test_router,
)
from app.infrastructure.config.settings import Settings, get_settings
from app.infrastructure.middleware.cors import register_cors_middleware

settings: Settings = get_settings()

app = FastAPI(debug=settings.debug)
register_cors_middleware(app, settings)
app.include_router(ceo_test_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=33333)
