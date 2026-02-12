"""
Tests unitaires de la liste chaînée.

Ces tests vérifient le comportement de base de la structure LinkedList :
- initialisation
- ajout en tête et en fin
- suppression
- parcours
"""

from src.domain.linked_list import LinkedList


def test_linked_list_initially_empty():
    """
    Vérifie qu'une liste nouvellement créée est vide.
    """
    ll = LinkedList()
    assert ll.is_empty() is True
    assert len(ll) == 0
    assert not ll.to_list()


def test_linked_list_prepend_and_iter():
    """
    Vérifie l'ajout en tête et l'ordre de parcours.
    """
    ll = LinkedList()
    ll.prepend(1)
    ll.prepend(2)
    ll.prepend(3)
    assert len(ll) == 3
    assert ll.to_list() == [3, 2, 1]


def test_linked_list_append_and_iter():
    """
    Vérifie l'ajout en fin et l'ordre de parcours.
    """
    ll = LinkedList()
    ll.append("a")
    ll.append("b")
    ll.append("c")
    assert ll.to_list() == ["a", "b", "c"]


def test_linked_list_pop_left():
    """
    Vérifie la suppression en tête de liste.
    """
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    assert ll.pop_left() == 10
    assert ll.pop_left() == 20
    assert ll.pop_left() is None
    assert ll.is_empty() is True
