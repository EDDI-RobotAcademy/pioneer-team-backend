import logging

from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

import app.infrastructure.database.orm_registry  # noqa: F401  (table registration)
from app.infrastructure.database.base import Base

logger = logging.getLogger(__name__)


def bootstrap_database(engine: Engine) -> None:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.exception("데이터베이스 연결에 실패했습니다. 부팅을 중단합니다.")
        raise

    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError:
        logger.exception("테이블 자동 생성에 실패했습니다. 부팅을 중단합니다.")
        raise
