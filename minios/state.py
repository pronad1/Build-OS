from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional


@dataclass
class ProcessInfo:
    pid: int
    name: str
    kind: str
    started_at: datetime = field(default_factory=datetime.now)
    running: bool = True


class MiniOSState:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.storage_root = project_root / "minios_storage"
        self.sandbox_root = self.storage_root / "sandbox"
        self.screenshot_root = self.storage_root / "screenshots"
        self.settings_path = self.storage_root / "settings.txt"
        self._next_pid = 1000
        self.processes: dict[int, ProcessInfo] = {}
        self.window_handles: dict[int, object] = {}
        self.current_user: Optional[str] = None
        self.theme_name = "Midnight"
        self.accent_name = "Teal"
        self.ensure_storage()
        self.start_process("MiniOS Shell", "system")

    def ensure_storage(self) -> None:
        self.sandbox_root.mkdir(parents=True, exist_ok=True)
        self.screenshot_root.mkdir(parents=True, exist_ok=True)
        (self.sandbox_root / "Documents").mkdir(parents=True, exist_ok=True)
        (self.sandbox_root / "Downloads").mkdir(parents=True, exist_ok=True)
        (self.sandbox_root / "Recycle Bin").mkdir(parents=True, exist_ok=True)
        if not self.settings_path.exists():
            self.settings_path.write_text("theme=Midnight\naccent=Teal\n", encoding="utf-8")

    @property
    def valid_credentials(self) -> dict[str, str]:
        return {"admin": "admin123", "student": "os2026"}

    def authenticate(self, username: str, password: str) -> bool:
        return self.valid_credentials.get(username) == password

    def start_process(self, name: str, kind: str) -> int:
        pid = self._next_pid
        self._next_pid += 1
        self.processes[pid] = ProcessInfo(pid=pid, name=name, kind=kind)
        return pid

    def bind_window(self, pid: int, window: object) -> None:
        self.window_handles[pid] = window

    def unbind_window(self, pid: int) -> None:
        self.window_handles.pop(pid, None)

    def end_process(self, pid: int) -> bool:
        info = self.processes.get(pid)
        if info is None or info.kind == "system":
            return False
        info.running = False
        window = self.window_handles.pop(pid, None)
        if window is not None and hasattr(window, "close"):
            try:
                window.close()
            except Exception:
                pass
        self.processes.pop(pid, None)
        return True

    def list_processes(self) -> list[ProcessInfo]:
        return sorted(self.processes.values(), key=lambda item: item.pid)

    def load_preferences(self) -> None:
        if not self.settings_path.exists():
            return
        for raw_line in self.settings_path.read_text(encoding="utf-8").splitlines():
            if "=" not in raw_line:
                continue
            key, value = raw_line.split("=", 1)
            key = key.strip().lower()
            value = value.strip()
            if key == "theme":
                self.theme_name = value or self.theme_name
            elif key == "accent":
                self.accent_name = value or self.accent_name

    def save_preferences(self) -> None:
        self.settings_path.write_text(
            f"theme={self.theme_name}\naccent={self.accent_name}\n",
            encoding="utf-8",
        )
