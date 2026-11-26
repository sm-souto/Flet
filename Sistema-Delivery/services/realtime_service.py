import threading
from typing import Callable


class RealtimeOrderWatcher:
    """Atualiza periodicamente a tela de pedidos enquanto a sessao estiver ativa."""

    def __init__(self, interval_seconds: int = 10) -> None:
        self._interval = max(5, interval_seconds)
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self, on_tick: Callable[[], None], is_active: Callable[[], bool]) -> None:
        """Inicia o monitoramento em segundo plano sem bloquear a interface."""
        self.stop()
        self._stop_event = threading.Event()

        def _worker() -> None:
            while not self._stop_event.wait(self._interval):
                if not is_active():
                    break
                try:
                    on_tick()
                except Exception:
                    pass

        self._thread = threading.Thread(target=_worker, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Encerra o monitoramento em segundo plano."""
        self._stop_event.set()
        self._thread = None
