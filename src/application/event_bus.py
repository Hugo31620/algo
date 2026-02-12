"""
Event bus implémentant le pattern Observer.

Ce module fournit un mécanisme simple de publication / abonnement
pour découpler les producteurs d'événements (workers) des consommateurs
(interface graphique, logs, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, DefaultDict, Type, TypeVar
from collections import defaultdict


class Event:  # pylint: disable=too-few-public-methods
    """
    Classe de base pour tous les événements.

    Cette classe est volontairement minimale et sert uniquement
    de type parent pour les événements transportant des données.
    """


@dataclass(frozen=True)
class ReadingLoaded(Event):
    """
    Événement émis lorsqu'une lecture météo a été chargée avec succès.

    Attributs :
        station : nom de la station concernée
        data : données météo associées (objet Station ou None)
    """

    station: str
    data: object


@dataclass(frozen=True)
class ReadingFailed(Event):
    """
    Événement émis lorsqu'une erreur survient lors du chargement
    des données météo d'une station.

    Attributs :
        station : nom de la station concernée
        error : message d'erreur associé
    """

    station: str
    error: str


E = TypeVar("E", bound=Event)
Handler = Callable[[Event], None]


class EventBus:
    """
    Bus d'événements simple implémentant le pattern Observer.

    Permet :
    - l'inscription de gestionnaires (observers)
    - la publication d'événements typés
    """

    def __init__(self) -> None:
        """
        Initialise le bus d'événements sans abonnés.
        """
        self._subscribers: DefaultDict[Type[Event], list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: Type[E], handler: Callable[[E], None]) -> None:
        """
        Abonne un gestionnaire à un type d'événement.

        Args:
            event_type : classe de l'événement à observer
            handler : fonction appelée lors de la publication
        """
        self._subscribers[event_type].append(handler)

    def publish(self, event: Event) -> None:
        """
        Publie un événement et notifie tous les abonnés correspondants.

        Args:
            event : événement à diffuser
        """
        for handler in self._subscribers[type(event)]:
            handler(event)
