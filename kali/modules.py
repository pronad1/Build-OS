from __future__ import annotations

import os
import shutil
import random
import platform
from pathlib import Path

from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QInputDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QGridLayout,
    QPlainTextEdit,
    QFormLayout
)



# =========================
# NOTEPAD
# =========================

class NotepadWindow(QMainWindow):

    def __init__(self,state,parent=None):

        super().__init__(parent)

        self.state=state
        self.path=None

        self.setWindowTitle("Notepad")
        self.resize(800,600)


        self.editor=QPlainTextEdit()

        self.editor.setFont(
            QFont("Consolas",12)
        )

        self.setCentralWidget(
            self.editor
        )


        bar=self.addToolBar("File")


        bar.addAction(
            "New File",
            self.new_file
        )


        bar.addAction(
            "Open File",
            self.open_file
        )


        bar.addAction(
            "Save File",
            self.save_file
        )



    def new_file(self):

        self.editor.clear()

        self.path=None

        self.setWindowTitle(
            "Notepad - New File"
        )



    def open_file(self):

        file,_=QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Text Files (*.txt)"
        )


        if file:

            self.path=Path(file)

            self.editor.setPlainText(
                self.path.read_text(
                encoding="utf-8"
                )
            )




    def save_file(self):

        if self.path is None:

            file,_=QFileDialog.getSaveFileName(
                self,
                "Save File",
                "",
                "Text Files (*.txt)"
            )


            if not file:
                return


            self.path=Path(file)



        self.path.write_text(
            self.editor.toPlainText(),
            encoding="utf-8"
        )



# =========================
# CALCULATOR
# =========================


class CalculatorWindow(QWidget):

    def __init__(self,parent=None):

        super().__init__(parent)

        self.exp=""

        self.setWindowTitle(
            "Calculator"
        )

        self.resize(400,500)


        layout=QVBoxLayout(self)


        self.display=QLineEdit()

        layout.addWidget(
            self.display
        )


        grid=QGridLayout()


        buttons=[
        "7","8","9","/",
        "4","5","6","*",
        "1","2","3","-",
        "0",".","=","+"
        ]


        for i,b in enumerate(buttons):

            btn=QPushButton(b)

            btn.clicked.connect(
                lambda x,v=b:self.click(v)
            )

            grid.addWidget(
                btn,
                i//4,
                i%4
            )


        layout.addLayout(grid)



    def click(self,v):

        if v=="=":

            try:
                self.display.setText(
                    str(eval(self.exp))
                )

            except:

                self.display.setText(
                    "Error"
                )

            self.exp=""

        else:

            self.exp+=v

            self.display.setText(
                self.exp
            )





# =========================
# FILE EXPLORER
# =========================


class FileExplorerWindow(QWidget):


    def __init__(self,state,parent=None):

        super().__init__(parent)


        self.state=state

        self.current=state.sandbox_root

        self.clipboard=None


        self.resize(
            950,600
        )


        self.setWindowTitle(
            "File Explorer"
        )


        self.build()

        self.refresh()




    def build(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1c23;
                color: #e0e0e0;
            }
            QLineEdit, QListWidget {
                background-color: #2a2e32;
                border: 1px solid #35bf5c;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton {
                background-color: #35bf5c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ea54f;
            }
        """)

        layout=QVBoxLayout(self)

        self.path=QLineEdit(str(self.current))
        self.path.setReadOnly(True)
        layout.addWidget(self.path)

        self.search=QLineEdit()
        self.search.setPlaceholderText("Search...")
        self.search.textChanged.connect(self.refresh)
        layout.addWidget(self.search)



        row=QHBoxLayout()


        buttons=[
               ("⬆ Up", self.go_up),
               ("New Folder",self.folder),
               ("New File",self.file),
               ("Rename",self.rename),
               ("Delete",self.delete),
               ("Copy",self.copy),
               ("Move",self.move)
                ]


        for name,func in buttons:

            b=QPushButton(name)

            b.clicked.connect(func)

            row.addWidget(b)


        layout.addLayout(row)



        self.list=QListWidget()
        self.list.itemDoubleClicked.connect(self.enter_folder)
        layout.addWidget(self.list)



    def refresh(self):
        self.list.clear()
        key=self.search.text().lower()

        for item in self.current.iterdir():
            if key in item.name.lower():
                icon = "📁 " if item.is_dir() else "📄 "
                i=QListWidgetItem(icon + item.name)
                i.setData(Qt.UserRole, str(item))
                self.list.addItem(i)

    def enter_folder(self, item):
        path = Path(item.data(Qt.UserRole))
        if path.is_dir():
            self.current = path
            self.path.setText(str(self.current))
            self.refresh()

    def go_up(self):
        if self.current != self.state.sandbox_root:
            self.current = self.current.parent
            self.path.setText(str(self.current))
            self.refresh()





    def selected(self):

        item=self.list.currentItem()

        if not item:
            return None

        return Path(
            item.data(Qt.UserRole)
        )



    def folder(self):

        name,ok=QInputDialog.getText(
            self,
            "Folder",
            "Name"
        )

        if ok:

            (self.current/name).mkdir()

            self.refresh()



    def file(self):

        name,ok=QInputDialog.getText(
            self,
            "File",
            "Name"
        )

        if ok:

            (self.current/name).write_text("")

            self.refresh()



    def rename(self):

        p=self.selected()

        if p:

            name,ok=QInputDialog.getText(
                self,
                "Rename",
                "New name"
            )

            if ok:

                p.rename(
                    p.parent/name
                )

                self.refresh()



    def delete(self):
        p=self.selected()
        if p:
            try:
                recycle_bin = self.state.sandbox_root / "Recycle Bin"
                recycle_bin.mkdir(exist_ok=True)
                dest = recycle_bin / p.name
                if dest.exists():
                    dest = recycle_bin / f"{p.name}_{random.randint(1000, 9999)}"
                shutil.move(str(p), str(dest))
                self.refresh()
            except Exception as e:
                QMessageBox.warning(self, "Delete Error", str(e))




    def copy(self):

        self.clipboard=self.selected()



def move(self):

    source=self.clipboard


    if source is None:

        QMessageBox.warning(
            self,
            "Move",
            "First select and Copy a file"
        )

        return



    folder,_=QInputDialog.getText(
        self,
        "Move File",
        "Destination Folder Name:"
    )


    if not folder:
        return



    destination = (
        self.current
        /
        folder
        /
        source.name
    )


    try:

        shutil.move(
            str(source),
            str(destination)
        )


        QMessageBox.information(
            self,
            "Move",
            "File moved successfully"
        )


        self.clipboard=None

        self.refresh()



    except Exception as e:

        QMessageBox.warning(
            self,
            "Error",
            str(e)
        )






# =========================
# TASK MANAGER
# =========================


class TaskManagerWindow(QWidget):

    def __init__(self,state,parent=None):

        super().__init__(parent)

        self.state=state

        self.resize(800,500)


        self.table=QTableWidget(
            0,6
        )


        self.table.setHorizontalHeaderLabels(
        [
        "PID",
        "Name",
        "Type",
        "CPU%",
        "RAM",
        "Status"
        ])


        layout=QVBoxLayout(self)

        layout.addWidget(
            self.table
        )


        btn=QPushButton(
            "Refresh"
        )

        btn.clicked.connect(
            self.refresh
        )

        layout.addWidget(btn)


        self.timer=QTimer()

        self.timer.timeout.connect(
            self.refresh
        )

        self.timer.start(2000)


        self.refresh()



    def refresh(self):

        data=self.state.list_processes()


        self.table.setRowCount(
            len(data)
        )


        for r,p in enumerate(data):

            values=[
            p.pid,
            p.name,
            p.kind,
            random.randint(1,30),
            random.randint(20,500),
            "Running"
            ]


            for c,v in enumerate(values):

                self.table.setItem(
                    r,c,
                    QTableWidgetItem(
                    str(v)
                    )
                )





# =========================
# SETTINGS
# =========================

class SettingsWindow(QWidget):

    def __init__(self,state,parent=None):

        super().__init__(parent)

        self.state=state


        self.setWindowTitle(
            "Settings"
        )

        self.resize(
            900,
            600
        )


        layout=QFormLayout(self)


        title=QLabel(
            "KALI Settings"
        )

        title.setStyleSheet(
            """
            font-size:26px;
            font-weight:bold;
            """
        )

        layout.addRow(
            title
        )



        layout.addRow(
            "OS Name",
            QLabel("KALI 1.0")
        )



        layout.addRow(
            "User",
            QLabel(
                state.current_user
            )
        )



        layout.addRow(
            "CPU",
            QLabel(
                platform.processor()
            )
        )



        layout.addRow(
            "System",
            QLabel(
                platform.system()
            )
        )


        layout.addRow(
            "Python Version",
            QLabel(
                platform.python_version()
            )
        )



        self.theme=QLineEdit()

        self.theme.setPlaceholderText(
            "Enter theme name"
        )


        layout.addRow(
            "Theme",
            self.theme
        )



        self.wallpaper=QLineEdit()
        self.wallpaper.setPlaceholderText("Wallpaper path")
        layout.addRow("Wallpaper", self.wallpaper)

        # Advanced Settings
        advanced_title = QLabel("Advanced Kali Options")
        advanced_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #35bf5c; margin-top: 15px;")
        layout.addRow(advanced_title)

        from PyQt5.QtWidgets import QComboBox, QCheckBox
        
        self.network_cb = QComboBox()
        self.network_cb.addItems(["eth0 (Wired)", "wlan0 (Wireless)", "lo (Loopback)"])
        layout.addRow("Active Interface", self.network_cb)

        self.security_cb = QComboBox()
        self.security_cb.addItems(["Standard", "High", "Paranoid"])
        layout.addRow("Security Level", self.security_cb)

        self.dev_mode = QCheckBox("Enable root access / Developer Mode")
        layout.addRow("Developer Mode", self.dev_mode)



        btn=QPushButton(
            "Save Settings"
        )


        btn.setMinimumHeight(
            45
        )


        btn.clicked.connect(
            self.save
        )


        layout.addWidget(
            btn
        )



    def save(self):

        self.state.theme_name = self.theme.text()
        self.state.wallpaper = self.wallpaper.text()
        
        # Persist advanced settings
        self.state.network_interface = self.network_cb.currentText()
        self.state.security_level = self.security_cb.currentText()
        self.state.developer_mode = self.dev_mode.isChecked()

        self.state.save_preferences()


        QMessageBox.information(
            self,
            "Settings",
            "Settings Saved"
        )

# =========================
# WEB BROWSER
# =========================

class BrowserWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chrome Browser")
        self.resize(1024, 768)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(5, 5, 5, 5)

        self.back_btn = QPushButton("◀")
        self.back_btn.setFixedSize(30, 30)
        self.back_btn.clicked.connect(self.go_back)
        toolbar.addWidget(self.back_btn)

        self.forward_btn = QPushButton("▶")
        self.forward_btn.setFixedSize(30, 30)
        self.forward_btn.clicked.connect(self.go_forward)
        toolbar.addWidget(self.forward_btn)

        self.reload_btn = QPushButton("↻")
        self.reload_btn.setFixedSize(30, 30)
        self.reload_btn.clicked.connect(self.reload)
        toolbar.addWidget(self.reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate)
        self.url_bar.setPlaceholderText("Enter URL or search Google...")
        toolbar.addWidget(self.url_bar)

        layout.addLayout(toolbar)

        # Web View
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.browser.urlChanged.connect(self.update_url)
        layout.addWidget(self.browser)

        self.setStyleSheet("""
            QWidget {
                background-color: #1a1c23;
                color: white;
            }
            QLineEdit {
                background-color: #2a2e32;
                color: white;
                border: 1px solid #35bf5c;
                border-radius: 15px;
                padding: 0px 15px;
                height: 30px;
            }
            QPushButton {
                background-color: transparent;
                color: #e0e0e0;
                font-size: 16px;
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #2a2e32;
            }
        """)

    def navigate(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            if "." in url and " " not in url:
                url = "https://" + url
            else:
                url = "https://www.google.com/search?q=" + url.replace(" ", "+")
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def go_back(self):
        self.browser.back()

    def go_forward(self):
        self.browser.forward()

    def reload(self):
        self.browser.reload()