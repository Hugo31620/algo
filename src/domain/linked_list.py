"""
Implémentation d'une liste chaînée simple.

Cette structure de données est utilisée pour stocker l'historique
des dernières consultations dans l'application météo.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterator, Optional, TypeVar

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    """
    Maillon de la liste chaînée.

    Attributs :
        value : valeur stockée dans le maillon
        next : référence vers le maillon suivant
    """

    value: T
    next: Optional["Node[T]"] = None


class LinkedList(Generic[T]):
    """
    Liste chaînée simple.

    Fonctionnalités :
    - ajout en tête (prepend)
    - ajout en fin (append)
    - suppression en tête (pop_left)
    - parcours séquentiel
    """

    def __init__(self) -> None:
        """
        Initialise une liste chaînée vide.
        """
        self._head: Optional[Node[T]] = None
        self._tail: Optional[Node[T]] = None
        self._size: int = 0

    def __len__(self) -> int:
        """
        Retourne le nombre d'éléments dans la liste.
        """
        return self._size

    def is_empty(self) -> bool:
        """
        Indique si la liste est vide.

        Returns:
            True si la liste est vide, False sinon.
        """
        return self._size == 0

    def prepend(self, value: T) -> None:
        """
        Ajoute un élément en tête de liste.

        Args:
            value: valeur à ajouter
        """
        node = Node(value=value, next=self._head)
        self._head = node
        if self._tail is None:
            self._tail = node
        self._size += 1

    def append(self, value: T) -> None:
        """
        Ajoute un élément en fin de liste.

        Args:
            value: valeur à ajouter
        """
        node = Node(value=value)
        if self._tail is None:
            self._head = node
            self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def pop_left(self) -> Optional[T]:
        """
        Retire et retourne l'élément en tête de liste.

        Returns:
            La valeur retirée ou None si la liste est vide.
        """
        if self._head is None:
            return None

        value = self._head.value
        self._head = self._head.next
        self._size -= 1

        if self._head is None:
            self._tail = None

        return value

    def __iter__(self) -> Iterator[T]:
        """
        Permet d'itérer sur les éléments de la liste.

        Yields:
            Les valeurs stockées dans la liste, dans l'ordre.
        """
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def to_list(self) -> list[T]:
        """
        Convertit la liste chaînée en liste Python.

        Returns:
            Liste contenant les mêmes éléments.
        """
        return list(iter(self))
