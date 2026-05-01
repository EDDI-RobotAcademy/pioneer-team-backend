"""ORM 모델 등록 일원화 모듈.

새 도메인의 ORM 모델을 추가할 때 이 모듈에 import 한 줄만 추가하면
부팅 시 ``Base.metadata`` 에 자동으로 반영되어 테이블이 생성된다.

이 모듈은 ``Base.metadata.create_all`` 이 호출되기 전에 import 되어야 한다.
"""

from app.domains.tracking.ingestion.infrastructure.orm.tracking_event_orm import (  # noqa: F401
    TrackingEventORM,
)
