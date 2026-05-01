from fastapi import FastAPI

from app.domains.ceo_test.adapter.inbound.api.ceo_test_router import (
    router as ceo_test_router,
)
from app.domains.tracking.ingestion.adapter.inbound.api.tracking_event_router import (
    create_tracking_event_router,
)
from app.infrastructure.config.settings import Settings, get_settings
from app.infrastructure.database.bootstrap import bootstrap_database
from app.infrastructure.database.engine import (
    create_database_engine,
    create_session_factory,
)
from app.infrastructure.database.session import make_session_dependency
from app.infrastructure.middleware.cors import register_cors_middleware

settings: Settings = get_settings()

engine = create_database_engine(settings)
session_factory = create_session_factory(engine)
get_db_session = make_session_dependency(session_factory)

bootstrap_database(engine)

app = FastAPI(debug=settings.debug)
register_cors_middleware(app, settings)
app.include_router(ceo_test_router)
app.include_router(create_tracking_event_router(get_db_session))


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=33333)
