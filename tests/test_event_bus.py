"""
Tests unitaires du module event_bus.

Ces tests vérifient le bon fonctionnement du bus d'événements
implémentant le pattern Observer.
"""

from src.application.event_bus import EventBus, ReadingLoaded, ReadingFailed


def test_event_bus_subscribe_and_publish_loaded():
    """
    Vérifie qu'un événement ReadingLoaded est correctement publié
    et reçu par les abonnés.
    """
    bus = EventBus()
    received = []

    def handler(evt: ReadingLoaded):
        received.append((evt.station, evt.data))

    bus.subscribe(ReadingLoaded, handler)
    bus.publish(ReadingLoaded(station="A", data={"x": 1}))

    assert received == [("A", {"x": 1})]


def test_event_bus_subscribe_and_publish_failed():
    """
    Vérifie qu'un événement ReadingFailed est correctement publié
    et reçu par les abonnés.
    """
    bus = EventBus()
    received = []

    def handler(evt: ReadingFailed):
        received.append((evt.station, evt.error))

    bus.subscribe(ReadingFailed, handler)
    bus.publish(ReadingFailed(station="B", error="boom"))

    assert received == [("B", "boom")]
