"""
Interface graphique Tkinter de l'application météo.

Ce module contient :
- un worker en thread séparé pour ne pas bloquer l'UI
- une file (Queue) pour les jobs
- un EventBus (Observer) pour diffuser les résultats
- une liste chaînée pour l'historique des consultations
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from threading import Thread
from queue import Queue, Empty

from src.application.station_directory_service import StationDirectoryService
from src.application.event_bus import EventBus, ReadingLoaded, ReadingFailed
from src.domain.linked_list import LinkedList


MISSING_TEXT = "Non disponible"


def fmt_value(text: Optional[str]) -> str:
    """
    Formate une valeur texte pour l'affichage.

    Args:
        text: valeur à afficher

    Returns:
        Valeur nettoyée ou texte 'Non disponible'.
    """
    if text is None:
        return MISSING_TEXT
    cleaned = str(text).strip()
    return cleaned if cleaned else MISSING_TEXT


def fmt_number(value, unit: str = "", nd: int = 1) -> str:
    """
    Formate une valeur numérique pour l'affichage.

    Args:
        value: valeur à convertir en float
        unit: unité à afficher (ex: ' mm')
        nd: nombre de décimales

    Returns:
        Chaîne formatée ou texte 'Non disponible'.
    """
    if value is None:
        return MISSING_TEXT
    try:
        float_value = float(value)
    except (TypeError, ValueError):
        return MISSING_TEXT
    return f"{float_value:.{nd}f}{unit}"


class MeteoWorker:  # pylint: disable=too-few-public-methods
    """
    Worker consommant une file de jobs et publiant des événements.

    Le worker tourne dans un thread séparé. Il appelle le service métier
    puis publie ReadingLoaded / ReadingFailed via l'EventBus.
    """

    def __init__(
        self,
        service: StationDirectoryService,
        bus: EventBus,
        job_queue: Queue[str],
    ):
        """
        Initialise le worker.

        Args:
            service: service applicatif de récupération météo
            bus: bus d'événements (Observer)
            job_queue: file des stations à charger
        """
        self._service = service
        self._bus = bus
        self._job_queue = job_queue

    def run_forever(self) -> None:
        """
        Boucle infinie consommant les jobs et publiant des événements.
        """
        while True:
            station = self._job_queue.get()
            try:
                data = self._service.get_latest_for_station(station)
                self._bus.publish(ReadingLoaded(station=station, data=data))
            except (RuntimeError, ValueError) as exc:
                self._bus.publish(ReadingFailed(station=station, error=str(exc)))
            finally:
                self._job_queue.task_done()


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class MeteoApp:
    """
    Application Tkinter.

    Cette classe contient l'état UI (widgets) et orchestre :
    - la soumission de jobs dans une Queue
    - la réception d'événements via un EventBus
    - l'actualisation de l'affichage
    """

    def __init__(self, service: StationDirectoryService):
        """
        Initialise l'application.

        Args:
            service: service applicatif principal
        """
        self.service = service

        self.history: LinkedList[str] = LinkedList()
        self.history_max_size = 20

        self.job_queue: Queue[str] = Queue()
        self.bus = EventBus()
        self.result_queue: Queue[object] = Queue()

        self.root = tk.Tk()
        self.root.title("Météo – Stations Toulouse")
        self.root.geometry("650x540")
        self.root.resizable(False, False)

        self._build_ui()
        self._wire_observers()
        self._start_worker()

        self.root.after(150, self._poll_results)

    def _wire_observers(self) -> None:
        """
        Abonne l'UI aux événements du bus.

        Les handlers pushent les événements dans result_queue afin que
        l'UI les traite dans le thread Tkinter.
        """

        def on_loaded(evt: ReadingLoaded) -> None:
            self.result_queue.put(evt)

        def on_failed(evt: ReadingFailed) -> None:
            self.result_queue.put(evt)

        self.bus.subscribe(ReadingLoaded, on_loaded)
        self.bus.subscribe(ReadingFailed, on_failed)

    def _start_worker(self) -> None:
        """
        Démarre le worker dans un thread daemon.
        """
        worker = MeteoWorker(
            service=self.service,
            bus=self.bus,
            job_queue=self.job_queue,
        )
        thread = Thread(target=worker.run_forever, daemon=True)
        thread.start()

    def _build_ui(self) -> None:
        """
        Construit l'interface graphique (widgets Tkinter).
        """
        title = ttk.Label(
            self.root,
            text="Stations météo – Toulouse Métropole",
            font=("Segoe UI", 14, "bold"),
        )
        title.pack(pady=15)

        frame_select = ttk.Frame(self.root)
        frame_select.pack(pady=10)

        ttk.Label(frame_select, text="Station :").pack(side=tk.LEFT, padx=5)

        self.station_var = tk.StringVar()
        self.station_combo = ttk.Combobox(
            frame_select,
            textvariable=self.station_var,
            state="readonly",
            width=35,
        )
        self.station_combo.pack(side=tk.LEFT)

        stations = self.service.get_station_names()
        self.station_combo["values"] = stations
        if stations:
            self.station_combo.current(0)
        else:
            messagebox.showwarning("Stations", "Aucune station disponible.")

        self.fetch_button = ttk.Button(
            self.root,
            text="Afficher la météo",
            command=self._enqueue_job,
        )
        self.fetch_button.pack(pady=10)

        self.status_label = ttk.Label(self.root, text="")
        self.status_label.pack(pady=2)

        self.result_frame = ttk.LabelFrame(self.root, text="Dernière mesure")
        self.result_frame.pack(fill="x", padx=20, pady=10)

        self.labels = {}
        for field in (
            "Timestamp",
            "Température",
            "Humidité",
            "Pression",
            "Pluie",
            "Vent",
            "Direction vent",
        ):
            row = ttk.Frame(self.result_frame)
            row.pack(fill="x", padx=10, pady=4)

            ttk.Label(row, text=f"{field} :", width=16).pack(side=tk.LEFT)
            value = ttk.Label(row, text=MISSING_TEXT)
            value.pack(side=tk.LEFT)
            self.labels[field] = value

        self.history_frame = ttk.LabelFrame(
            self.root,
            text="Historique (dernières consultations)",
        )
        self.history_frame.pack(fill="both", expand=False, padx=20, pady=10)

        self.history_listbox = tk.Listbox(self.history_frame, height=6)
        self.history_listbox.pack(fill="both", padx=10, pady=8)

    def _enqueue_job(self) -> None:
        """
        Envoie une demande de chargement dans la file de jobs.
        """
        station = self.station_var.get()
        if not station:
            messagebox.showwarning("Station", "Sélectionne une station.")
            return

        self.fetch_button.config(state="disabled")
        self.status_label.config(text="Chargement en cours...")
        self.job_queue.put(station)

    def _poll_results(self) -> None:
        """
        Poll la file des résultats et met à jour l'UI.
        """
        try:
            while True:
                evt = self.result_queue.get_nowait()

                self.fetch_button.config(state="normal")
                self.status_label.config(text="")

                if isinstance(evt, ReadingFailed):
                    messagebox.showerror("Erreur", evt.error)
                    continue

                if isinstance(evt, ReadingLoaded):
                    if evt.data is None:
                        messagebox.showwarning(
                            "Aucune donnée",
                            "Aucune donnée disponible pour cette station.",
                        )
                        continue
                    self._render_data(evt.station, evt.data)

        except Empty:
            pass
        finally:
            self.root.after(150, self._poll_results)

    def _push_history(self, station_name: str, timestamp_str: str) -> None:
        """
        Ajoute une entrée à l'historique (liste chaînée), taille limitée.
        """
        entry = f"{station_name} | {timestamp_str}"
        self.history.prepend(entry)

        if len(self.history) > self.history_max_size:
            entries = self.history.to_list()[: self.history_max_size]
            self.history = LinkedList()
            for item in reversed(entries):
                self.history.prepend(item)

        self._refresh_history_view()

    def _refresh_history_view(self) -> None:
        """
        Rafraîchit l'affichage de l'historique dans la listbox.
        """
        self.history_listbox.delete(0, tk.END)
        for entry in self.history:
            self.history_listbox.insert(tk.END, entry)

    def _render_data(self, station: str, data) -> None:
        """
        Met à jour les labels avec les données récupérées.

        Args:
            station: nom de la station
            data: objet Station (domain)
        """
        timestamp_str = str(getattr(data, "timestamp", ""))

        self.labels["Timestamp"].config(text=fmt_value(timestamp_str))
        self.labels["Température"].config(
            text=fmt_value(getattr(data.temperature, "value", None))
        )
        self.labels["Humidité"].config(
            text=fmt_value(getattr(data.humidity, "value", None))
        )
        self.labels["Pression"].config(
            text=fmt_value(getattr(data.pressure, "value", None))
        )

        self.labels["Pluie"].config(
            text=fmt_number(getattr(data, "rain", None), " mm", 1)
        )
        self.labels["Vent"].config(
            text=fmt_number(getattr(data, "wind_speed", None), " km/h", 1)
        )
        self.labels["Direction vent"].config(
            text=fmt_number(getattr(data, "wind_direction", None), "°", 0)
        )

        self._push_history(station, timestamp_str)

    def run(self) -> None:
        """
        Lance la boucle principale Tkinter.
        """
        self.root.mainloop()
