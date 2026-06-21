from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .widgets import GanttChartWidget, GanttSegment


@dataclass
class ProcessRow:
    name: str
    arrival: int
    burst: int
    priority: int


class CpuSchedulerWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            self.windowFlags()
            | Qt.Window
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
            | Qt.WindowCloseButtonHint
        )
        self.setWindowTitle("CPU Scheduler")
        self.setMinimumSize(940, 640)
        self.process_rows: list[ProcessRow] = [
            ProcessRow("P1", 0, 7, 2),
            ProcessRow("P2", 2, 4, 1),
            ProcessRow("P3", 4, 1, 3),
            ProcessRow("P4", 5, 4, 2),
        ]
        self._build_ui()
        self.refresh_table()
        self.refresh_chart()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        header = QLabel("CPU Scheduling Visualizer")
        header.setObjectName("SectionHeader")
        root.addWidget(header)

        controls = QHBoxLayout()
        self.algorithm = QComboBox()
        self.algorithm.addItems(["FCFS", "SJF", "Round Robin", "Priority"])
        self.quantum = QSpinBox()
        self.quantum.setRange(1, 20)
        self.quantum.setValue(2)
        add_button = QPushButton("Add Process")
        add_button.clicked.connect(self.add_process_row)
        remove_button = QPushButton("Remove Selected")
        remove_button.clicked.connect(self.remove_selected_row)
        run_button = QPushButton("Run Scheduling")
        run_button.clicked.connect(self.refresh_chart)
        controls.addWidget(QLabel("Algorithm"))
        controls.addWidget(self.algorithm)
        controls.addWidget(QLabel("Quantum"))
        controls.addWidget(self.quantum)
        controls.addWidget(add_button)
        controls.addWidget(remove_button)
        controls.addStretch(1)
        controls.addWidget(run_button)
        root.addLayout(controls)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Process", "Arrival", "Burst", "Priority"])
        self.table.verticalHeader().setVisible(False)
        root.addWidget(self.table)

        self.table.setSortingEnabled(False)

        self.gantt = GanttChartWidget()
        root.addWidget(self.gantt)

        self.summary = QLabel()
        self.summary.setWordWrap(True)
        root.addWidget(self.summary)

    def refresh_table(self) -> None:
        self.table.setRowCount(len(self.process_rows))
        for row_index, row in enumerate(self.process_rows):
            values = [row.name, str(row.arrival), str(row.burst), str(row.priority)]
            for column_index, value in enumerate(values):
                self.table.setItem(row_index, column_index, QTableWidgetItem(value))

    def add_process_row(self) -> None:
        self.sync_from_table()
        next_index = len(self.process_rows) + 1
        self.process_rows.append(ProcessRow(f"P{next_index}", next_index - 1, 1, 1))
        self.refresh_table()

    def remove_selected_row(self) -> None:
        self.sync_from_table()
        row = self.table.currentRow()
        if row < 0 or row >= len(self.process_rows):
            return
        self.process_rows.pop(row)
        self.refresh_table()

    def sync_from_table(self) -> None:
        rows: list[ProcessRow] = []
        for row_index in range(self.table.rowCount()):
            name_item = self.table.item(row_index, 0)
            arrival_item = self.table.item(row_index, 1)
            burst_item = self.table.item(row_index, 2)
            priority_item = self.table.item(row_index, 3)
            if name_item is None or arrival_item is None or burst_item is None or priority_item is None:
                continue
            name = name_item.text().strip() or f"P{row_index + 1}"
            try:
                arrival = max(0, int(arrival_item.text()))
                burst = max(1, int(burst_item.text()))
                priority = max(0, int(priority_item.text()))
            except ValueError:
                continue
            rows.append(ProcessRow(name, arrival, burst, priority))
        if rows:
            self.process_rows = rows

    def refresh_chart(self) -> None:
        self.sync_from_table()
        algorithm = self.algorithm.currentText()
        segments, summary = self._schedule(algorithm)
        self.gantt.set_segments(segments)
        self.summary.setText(summary)

    def _schedule(self, algorithm: str) -> tuple[list[GanttSegment], str]:
        if algorithm == "FCFS":
            segments, stats = self._fcfs()
        elif algorithm == "SJF":
            segments, stats = self._sjf()
        elif algorithm == "Round Robin":
            segments, stats = self._round_robin(self.quantum.value())
        else:
            segments, stats = self._priority()
        average_wait = sum(stat[1] for stat in stats) / max(1, len(stats))
        average_turnaround = sum(stat[2] for stat in stats) / max(1, len(stats))
        summary = (
            f"Algorithm: {algorithm} | Average waiting time: {average_wait:.2f} | "
            f"Average turnaround time: {average_turnaround:.2f}"
        )
        return segments, summary

    def _palette(self) -> list[QColor]:
        return [QColor("#22d3ee"), QColor("#f97316"), QColor("#a78bfa"), QColor("#34d399"), QColor("#facc15")]

    def _fcfs(self) -> tuple[list[GanttSegment], list[tuple[str, int, int]]]:
        time = 0
        segments: list[GanttSegment] = []
        stats: list[tuple[str, int, int]] = []
        palette = self._palette()
        for index, row in enumerate(sorted(self.process_rows, key=lambda item: (item.arrival, item.name))):
            time = max(time, row.arrival)
            start = time
            end = start + row.burst
            waiting = start - row.arrival
            turnaround = end - row.arrival
            stats.append((row.name, waiting, turnaround))
            segments.append(GanttSegment(row.name, start, end, palette[index % len(palette)]))
            time = end
        return segments, stats

    def _sjf(self) -> tuple[list[GanttSegment], list[tuple[str, int, int]]]:
        remaining = sorted(self.process_rows, key=lambda item: (item.arrival, item.burst, item.name))
        time = 0
        segments: list[GanttSegment] = []
        finished: dict[str, tuple[int, int]] = {}
        palette = self._palette()
        while remaining:
            ready = [row for row in remaining if row.arrival <= time]
            if not ready:
                time = remaining[0].arrival
                continue
            current = min(ready, key=lambda row: (row.burst, row.arrival, row.name))
            start = time
            end = start + current.burst
            segments.append(GanttSegment(current.name, start, end, palette[len(segments) % len(palette)]))
            finished[current.name] = (start - current.arrival, end - current.arrival)
            time = end
            remaining.remove(current)
        stats = [(name, waiting, turnaround) for name, (waiting, turnaround) in finished.items()]
        return segments, stats

    def _round_robin(self, quantum: int) -> tuple[list[GanttSegment], list[tuple[str, int, int]]]:
        timeline = {row.name: row.burst for row in self.process_rows}
        arrival = {row.name: row.arrival for row in self.process_rows}
        completion: dict[str, int] = {}
        queue: list[str] = []
        time = 0
        palette = self._palette()
        ordered = sorted(self.process_rows, key=lambda row: (row.arrival, row.name))
        segments: list[GanttSegment] = []
        while timeline or queue:
            while ordered and ordered[0].arrival <= time:
                queue.append(ordered.pop(0).name)
            if not queue:
                if ordered:
                    time = ordered[0].arrival
                    continue
                break
            name = queue.pop(0)
            slice_time = min(quantum, timeline[name])
            start = time
            end = time + slice_time
            segments.append(GanttSegment(name, start, end, palette[len(segments) % len(palette)]))
            time = end
            timeline[name] -= slice_time
            while ordered and ordered[0].arrival <= time:
                queue.append(ordered.pop(0).name)
            if timeline[name] > 0:
                queue.append(name)
            else:
                completion[name] = time
                del timeline[name]
        stats = []
        for row in self.process_rows:
            turn = completion.get(row.name, time) - row.arrival
            wait = turn - row.burst
            stats.append((row.name, wait, turn))
        return segments, stats

    def _priority(self) -> tuple[list[GanttSegment], list[tuple[str, int, int]]]:
        remaining = list(self.process_rows)
        time = 0
        segments: list[GanttSegment] = []
        stats: list[tuple[str, int, int]] = []
        palette = self._palette()
        while remaining:
            ready = [row for row in remaining if row.arrival <= time]
            if not ready:
                time = min(row.arrival for row in remaining)
                continue
            current = min(ready, key=lambda row: (row.priority, row.arrival, row.name))
            start = time
            end = start + current.burst
            segments.append(GanttSegment(current.name, start, end, palette[len(segments) % len(palette)]))
            stats.append((current.name, start - current.arrival, end - current.arrival))
            time = end
            remaining.remove(current)
        return segments, stats
