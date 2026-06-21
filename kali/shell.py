from __future__ import annotations

import sys
import os

from pathlib import Path

from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox
)

from .modules import (
    FileExplorerWindow,
    NotepadWindow,
    CalculatorWindow,
    TaskManagerWindow,
    SettingsWindow,
    BrowserWindow
)

from .memory_manager import MemoryManagerWindow
from .scheduler import CpuSchedulerWindow
from .terminal import TerminalWindow
from .state import KaliState



# ================= LOGIN =================


class LoginDialog(QDialog):

    def __init__(self,state,parent=None):
        super().__init__(parent)
        self.state=state
        
        self.setWindowTitle("KALI Login")
        self.resize(500,350)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1c23;
            }
            QLabel {
                color: #e0e0e0;
            }
            QLineEdit {
                background-color: #2a2e32;
                color: #e0e0e0;
                border: 1px solid #35bf5c;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #35bf5c;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2ea54f;
            }
        """)

        layout=QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title=QLabel("KALI")
        title.setFont(QFont("Arial",36,QFont.Bold))
        title.setStyleSheet("color: #35bf5c;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.user=QLineEdit()
        self.user.setPlaceholderText("Username")
        self.user.setMinimumHeight(45)

        self.password=QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumHeight(45)

        layout.addWidget(self.user)
        layout.addWidget(self.password)

        btn=QPushButton("LOGIN")
        btn.setMinimumHeight(45)
        btn.clicked.connect(self.login)
        layout.addWidget(btn)

        self.msg=QLabel()
        self.msg.setAlignment(Qt.AlignCenter)
        self.msg.setStyleSheet("color: #ff5555;")
        layout.addWidget(self.msg)



    def login(self):

        if self.state.authenticate(
            self.user.text(),
            self.password.text()
        ):

            self.state.current_user=self.user.text()

            self.accept()

        else:
            self.msg.setText("Invalid Login")






# ================= DESKTOP =================


class DesktopLauncher(QMainWindow):


    def __init__(self,state):

        super().__init__()

        self.state=state

        self.windows={}


        self.resize(1400,850)

        self.setWindowTitle(
            "KALI Desktop"
        )

        self.build()




    def build(self):


        central=QWidget()

        self.setCentralWidget(central)


        root=QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)



        # ================= DESKTOP =================

        desktop = QFrame()
        desktop_layout = QGridLayout(desktop)
        desktop_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        desktop_layout.setSpacing(20)
        desktop_layout.setContentsMargins(20, 20, 20, 20)

        apps = [
            ("📁", "File", self.open_file_explorer),
            ("📝", "Notepad", self.open_notepad),
            ("🧮", "Calculator", self.open_calculator),
            ("📊", "Task", self.open_task_manager),
            ("🧠", "Memory", self.open_memory_manager),
            ("📋", "Scheduler", self.open_scheduler),
            ("⚙", "Settings", self.open_settings),
            ("💻", "Terminal", self.open_terminal),
            ("🌐", "Chrome", self.open_browser)
        ]

        for i, (icon, name, func) in enumerate(apps):
            box = QVBoxLayout()
            box.setAlignment(Qt.AlignCenter)
            btn = QPushButton(icon)
            btn.setFixedSize(70, 70)
            btn.setFont(QFont("Arial", 36))
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 40);
                    border-radius: 10px;
                }
            """)
            btn.clicked.connect(func)
            
            label = QLabel(name)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: white; font-weight: bold; font-family: Arial; background: transparent;")
            
            box.addWidget(btn)
            box.addWidget(label)
            
            w = QWidget()
            w.setFixedSize(100, 110)
            w.setLayout(box)
            
            desktop_layout.addWidget(w, i % 5, i // 5)

        root.addWidget(desktop)





        # ================= TASKBAR =================

        task = QFrame()
        task.setFixedHeight(45)

        bar = QHBoxLayout(task)
        bar.setContentsMargins(10, 0, 15, 0)

        start = QPushButton("🐧 Start")
        start.setFixedSize(100, 32)
        start.setFont(QFont("Arial", 11, QFont.Bold))
        start.setStyleSheet("""
            QPushButton {
                background: #35bf5c;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #2ea54f;
            }
            QPushButton:pressed {
                background: #248c40;
            }
        """)
        start.clicked.connect(self.power_menu)

        bar.addWidget(start)
        
        self.taskbar_apps_layout = QHBoxLayout()
        self.taskbar_apps_layout.setSpacing(5)
        bar.addLayout(self.taskbar_apps_layout)

        bar.addStretch()

        self.clock = QLabel()
        self.clock.setStyleSheet("color: white; font-weight: bold;")
        bar.addWidget(self.clock)

        root.addWidget(task)



        self.timer=QTimer(self)

        self.timer.timeout.connect(
            self.update_clock
        )

        self.timer.start(1000)



        # BACKGROUND IMAGE


        # =========================
        # BACKGROUND IMAGE FIX
        # =========================

        img = (Path(__file__).resolve().parents[1] / "image" / "picture.png").as_posix()

        central.setObjectName("central_widget")
        central.setStyleSheet(f"""
        QWidget#central_widget {{
            border-image: url("{img}") 0 0 0 0 stretch stretch;
        }}
        """)

        desktop.setStyleSheet("""
        QFrame {
            background: transparent;
        }
        """)

        task.setStyleSheet("""
        QFrame {
            background: #1a1c23;
            border-top: 1px solid #2a2e32;
        }
        """)
    def update_clock(self):
        self.clock.setText(
            QDateTime.currentDateTime()
            .toString("hh:mm:ss")
        )

        # Clear existing taskbar apps
        for i in reversed(range(self.taskbar_apps_layout.count())): 
            widget = self.taskbar_apps_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
                
        # Populate with running processes
        for proc in self.state.list_processes():
            if proc.kind == "system" or not proc.running:
                continue
                
            btn = QPushButton(f" {proc.name} ")
            btn.setFixedHeight(28)
            btn.setStyleSheet("""
                QPushButton {
                    background: #2a2e32;
                    color: white;
                    border: 1px solid #1a1c23;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background: #3a3f44;
                }
            """)
            # If clicked, focus the window
            # Can't easily pass it cleanly in a loop without a closure, so we just make it cosmetic for now,
            # or we could find the PID in self.windows.
            pid = proc.pid
            btn.clicked.connect(lambda _, p=pid: self.windows[p].raise_() if p in self.windows else None)
            
            self.taskbar_apps_layout.addWidget(btn)





    # =============== LAUNCH ===============


    def launch(self,key,obj,name):

        if key in self.windows:

            self.windows[key].show()
            return


        pid=self.state.start_process(
            name,
            "RUNNING"
        )


        self.state.bind_window(
            pid,
            obj
        )


        obj.destroyed.connect(
            lambda:self.state.end_process(pid)
        )


        self.windows[key]=obj


        obj.resize(
            900,
            600
        )


        obj.show()





    def open_file_explorer(self):

        self.launch(
        "file",
        FileExplorerWindow(self.state),
        "FileExplorer.exe"
        )


    def open_notepad(self):

        self.launch(
        "note",
        NotepadWindow(self.state),
        "Notepad.exe"
        )


    def open_calculator(self):

        self.launch(
        "calc",
        CalculatorWindow(),
        "Calculator.exe"
        )


    def open_task_manager(self):

        self.launch(
        "task",
        TaskManagerWindow(self.state),
        "TaskManager.exe"
        )


    def open_memory_manager(self):

        self.launch(
        "memory",
        MemoryManagerWindow(),
        "Memory.exe"
        )


    def open_scheduler(self):

        self.launch(
        "scheduler",
        CpuSchedulerWindow(),
        "Scheduler.exe"
        )


    def open_settings(self):

        self.launch(
        "settings",
        SettingsWindow(self.state),
        "Settings.exe"
        )


    def open_terminal(self):
        self.launch(
        "terminal",
        TerminalWindow(self.state),
        "Terminal.exe"
        )

    def open_browser(self):
        self.launch(
        "browser",
        BrowserWindow(),
        "Chrome.exe"
        )





    def power_menu(self):

        msg=QMessageBox(self)

        msg.setWindowTitle("Power")


        btn=msg.addButton(
            "Shutdown",
            QMessageBox.AcceptRole
        )

        msg.exec_()


        if msg.clickedButton()==btn:
            QApplication.quit()





# ================= RUN =================


def run_app():

    app=QApplication([])


    state=KaliState(
        Path(__file__).resolve().parents[1]
    )


    state.load_preferences()



    login=LoginDialog(state)


    if login.exec_()!=QDialog.Accepted:
        return



    desktop=DesktopLauncher(state)

    desktop.show()


    app.exec_()