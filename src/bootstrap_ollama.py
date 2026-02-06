# bootstrap_ollama.py
from __future__ import annotations

import os
import subprocess
import time
from urllib.request import urlopen
from urllib.error import URLError


def _default_ollama_check_url(ollama_host: str) -> str:
    # Пример: http://127.0.0.1:11434/api/tags
    return ollama_host.rstrip("/") + "/api/tags"


def is_ollama_up(ollama_host: str, timeout_sec: float = 2.0) -> bool:
    url = _default_ollama_check_url(ollama_host)
    try:
        with urlopen(url, timeout=timeout_sec) as resp:
            return 200 <= resp.status < 300
    except Exception:
        return False


def try_start_ollama_serve() -> None:
    """
    Пытаемся запустить `ollama serve` в фоне.
    Если Ollama уже работает как сервис — команда может просто завершиться/не помешает.
    """
    creationflags = 0
    # скрыть окно на Windows
    if os.name == "nt":
        creationflags = subprocess.CREATE_NO_WINDOW  # type: ignore[attr-defined]

    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
        )
    except Exception:
        # если ollama не в PATH или не установлена — просто молча
        return


def ensure_ollama_running(ollama_host: str, wait_seconds: int = 30) -> bool:
    """
    Возвращает True, если Ollama доступна.
    """
    if is_ollama_up(ollama_host):
        return True

    try_start_ollama_serve()

    t0 = time.time()
    while time.time() - t0 < wait_seconds:
        if is_ollama_up(ollama_host):
            return True
        time.sleep(1)

    return False