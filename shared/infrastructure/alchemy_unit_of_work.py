from __future__ import annotations
from typing import Callable

from sqlalchemy.orm.session import Session

from models import session_factory
from shared.domain.unit_of_work import UnitOfWork


class AlchemyUnitOfWork(UnitOfWork):
    """
    UnitOfWork Alchemy implementation. Uses Alchemy Sessions under the hood.
    """

    session: Session

    def __init__(
        self, _session_factory: Callable[[], Session] = session_factory
    ) -> None:
        super().__init__()
        self._session_factory = _session_factory

    def __enter__(self):
        self.session = self._session_factory()
        return self

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
