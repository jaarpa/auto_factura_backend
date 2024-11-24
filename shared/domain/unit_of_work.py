from __future__ import annotations

from abc import abstractmethod
from contextlib import AbstractContextManager
from typing import TypeVar

from shared.domain.entity import Entity
from shared.domain.repository import Repository

E = TypeVar("E", bound=Entity)


class UnitOfWork(AbstractContextManager):
    """
    Provides a session that will be used in the context of this unit of work.
    Provides a atomic operation and a stable persistence state to work from.
    """

    def __enter__(self) -> UnitOfWork:
        """Return `self` upon entering the runtime context."""
        return self

    @abstractmethod
    def __exit__(self, *args):
        """
        Reverts all changes to db on exit. Only changes that were committed
        will remain.
        """
        self.rollback()

    @abstractmethod
    def commit(self):
        """
        Commits the current transaction.
        """

    @abstractmethod
    def rollback(self):
        """
        Aborts the current transaction.
        Leaves the persistence state as when the last commit was done.
        """

    @abstractmethod
    def add(self, entity_instance: E):
        """
        Adds the provided entity_instance to the session.
        This can be used to create or update entities.
        The entity will not persisted till session commit by the unit of work.

        :param entity_instance: Updated entity instance.
        """

    @abstractmethod
    def get_repository(self, entity_class: type[E]) -> Repository[E]:
        """
        Returns the repository to manage the `entity_class` with the same
        session as the current uow.

        :param entity_class: Entity class to be managed
        :return: Repository that manages the entity class
        """