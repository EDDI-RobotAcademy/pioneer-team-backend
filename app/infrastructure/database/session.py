from collections.abc import Callable, Iterator

from sqlalchemy.orm import Session, sessionmaker


def make_session_dependency(
    session_factory: sessionmaker[Session],
) -> Callable[[], Iterator[Session]]:
    def get_session() -> Iterator[Session]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    return get_session
