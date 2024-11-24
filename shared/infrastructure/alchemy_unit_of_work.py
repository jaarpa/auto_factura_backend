from __future__ import annotations

from typing import Callable, TypeVar

from sqlalchemy.orm.session import Session

from models import session_factory
from shared.domain.entity import Entity
from shared.domain.repository import Repository
from shared.domain.unit_of_work import UnitOfWork
from shared.infrastructure.alchemy_repository import AlchemyRepository

E = TypeVar("E", bound=Entity)


class AlchemyUnitOfWork(UnitOfWork):
    """
    UnitOfWork Alchemy implementation. Uses Alchemy Sessions under the hood.
    """

    session: Session
    """
    Session will only be populated till the unit of work enters into a context.
    """

    def __init__(
        self, _session_factory: Callable[[], Session] = session_factory
    ) -> None:
        super().__init__()
        self._session_factory = _session_factory

    def __enter__(self):
        self.session = self._session_factory()
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def add(self, entity_instance: E):
        self.session.add(entity_instance)

    def get_repository(self, entity_class: type[E]) -> Repository[E]:
        return AlchemyRepository[entity_class](entity_class, self.session)
