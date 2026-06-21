from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QFont
from PyQt5.QtWidgets import QWidget


@dataclass
class GanttSegment:
    label: str
    start: int
    end: int
    color: QColor


class GanttChartWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.segments: list[GanttSegment] = []
        self.total_time = 0
        self.setMinimumHeight(170)

    def set_segments(self, segments: Iterable[GanttSegment]) -> None:
        self.segments = list(segments)
        self.total_time = max((segment.end for segment in self.segments), default=0)
        self.update()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("#101826"))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#162236"))
        painter.drawRoundedRect(self.rect().adjusted(8, 8, -8, -8), 16, 16)

        if not self.segments or self.total_time <= 0:
            painter.setPen(QColor("#9fb3c8"))
            painter.drawText(self.rect(), Qt.AlignCenter, "Run a schedule to render the Gantt chart")
            return

        left = 28
        top = 58
        width = max(10, self.width() - 56)
        lane_height = 50
        scale = width / self.total_time

        painter.setPen(QPen(QColor("#334155"), 1))
        painter.drawLine(left, top + lane_height, left + width, top + lane_height)

        for segment in self.segments:
            seg_left = left + int(segment.start * scale)
            seg_width = max(28, int((segment.end - segment.start) * scale))
            rect = event.rect().adjusted(0, 0, 0, 0)
            del rect
            painter.setBrush(QBrush(segment.color))
            painter.setPen(QPen(QColor("#0b1220"), 1))
            painter.drawRoundedRect(seg_left, top, seg_width, lane_height, 10, 10)
            painter.setPen(QColor("#0b1220"))
            painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
            painter.drawText(seg_left + 8, top + 20, segment.label)
            painter.drawText(seg_left + 8, top + 38, f"{segment.start}-{segment.end}")

        painter.setPen(QColor("#cbd5e1"))
        painter.setFont(QFont("Segoe UI", 9))
        tick_count = min(self.total_time, 12)
        if tick_count <= 0:
            tick_count = 1
        for tick in range(tick_count + 1):
            value = round(self.total_time * tick / tick_count)
            x = left + int(value * scale)
            painter.drawLine(x, top + lane_height, x, top + lane_height + 8)
            painter.drawText(x - 8, top + lane_height + 24, str(value))


class MemoryBarWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.partitions: list[tuple[str, int, QColor]] = []
        self.used_total = 0
        self.setMinimumHeight(180)

    def set_partitions(self, partitions: list[tuple[str, int, QColor]]) -> None:
        self.partitions = partitions
        self.used_total = sum(size for _, size, _ in partitions)
        self.update()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("#0f172a"))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#172554"))
        painter.drawRoundedRect(self.rect().adjusted(8, 8, -8, -8), 16, 16)

        if not self.partitions:
            painter.setPen(QColor("#94a3b8"))
            painter.drawText(self.rect(), Qt.AlignCenter, "Visual memory map appears here")
            return

        inner = self.rect().adjusted(24, 24, -24, -24)
        total = max(1, self.used_total)
        x = inner.x()
        y = inner.y()
        height = inner.height()
        width = inner.width()

        painter.setFont(QFont("Segoe UI", 9))
        for name, size, color in self.partitions:
            block_width = max(40, int(width * size / total))
            block_width = min(block_width, inner.right() - x)
            painter.setBrush(color)
            painter.setPen(QPen(QColor("#0b1220"), 1))
            painter.drawRoundedRect(x, y, block_width - 4, height, 12, 12)
            painter.setPen(QColor("#0b1220"))
            painter.drawText(x + 10, y + height // 2 - 5, name)
            painter.drawText(x + 10, y + height // 2 + 12, f"{size} KB")
            x += block_width
            if x >= inner.right():
                break
