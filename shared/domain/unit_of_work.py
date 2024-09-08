from __future__ import annotations
from abc import abstractmethod
from contextlib import AbstractContextManager


class UnitOfWork(AbstractContextManager):
    """
    Provides a session that will be used in the context of this unit of work.
    Providesa atomic operation and a stable persistence state to work from.
    """

    @abstractmethod
    def __exit__(self, *args):
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
