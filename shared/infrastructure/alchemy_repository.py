from collections.abc import Collection
from typing import Callable, Optional, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm.session import Session

from models import session_factory
from shared.domain.entity import Entity
from shared.domain.repository import Repository

E_co = TypeVar("E_co", bound=Entity, covariant=True)


class AlchemyRepository[E_co](Repository[E_co]):
    """
    Generic repository implementation with sqlalchemy.
    """

    _session: Session

    def __init__(
        self,
        entity_class: type[E_co],
        session: Optional[Session] = None,
        _session_factory: Callable[[], Session] = session_factory,
    ):
        self._entity_class = entity_class
        self._session = session or _session_factory()

    def get(self, pk: UUID) -> E_co | None:
        return self._session.get(self._entity_class, pk)

    def filter_by_fields(self, **kwargs) -> Collection[E_co]:
        stmt = select(self._entity_class).filter_by(**kwargs)
        results = self._session.scalars(stmt).all()
        return results

    def get_by_fields(self, **kwargs) -> E_co | None:
        stmt = select(self._entity_class).filter_by(**kwargs)
        results = self._session.scalar(stmt)
        return results

    def add(self, entity_instance: E_co):
        self._session.add(entity_instance)
    
    def all(self) -> Collection[E_co]:
        """_summary_
        Retrieves all entries of entity from the database.

        Returns:
            Collection[E_co]: _description_
        """
        stmt = select(self._entity_class)
        results = self._session.scalars(stmt).all()
        return results
    
