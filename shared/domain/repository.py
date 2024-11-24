from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol, TypeVar, runtime_checkable
from uuid import UUID

from shared.domain.entity import Entity

E_co = TypeVar("E_co", bound=Entity, covariant=True)


@runtime_checkable
class Repository[E_co](Protocol):
    """
    Generic repository used to get an entity from the database.
    """

    @abstractmethod
    def get(self, pk: UUID) -> E_co | None:
        """
        Gets entity by `id`

        :param pk: Entity pk.
        :return: Entity instance
        """

    @abstractmethod
    def filter_by_fields(self, **kwargs) -> Collection[E_co]:
        """
        Filters the repository entity by the kwargs.
        All the attributes of the entity will match the provided field=values
        in kwargs.

        :return: Collection of entities that matched in all the provided kwargs.
        """

    @abstractmethod
    def get_by_fields(self, **kwargs) -> E_co | None:
        """
        Gets the one entity that matches all the attributes provided as field=values
        in kwargs.
        This expects that only one entity matches the arguments, an Exception is raised
        if more than one is found.

        :return: One entities that matched in all the provided kwargs.
        """

    @abstractmethod
    def add(self, entity_instance: E_co):
        """
        Adds the of the provided entity_instance to the session.
        This can be used to create or update entities.
        The entity will not persisted till session commit by the unit of work.

        :param entity_instance: Updated entity instance.
        """
