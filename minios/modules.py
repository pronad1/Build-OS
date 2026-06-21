from __future__ import annotations

import os
import shutil
import random
import platform
from pathlib import Path

from PyQt5.QtCore import Qt, QTimer
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

        layout=QVBoxLayout(self)


        self.path=QLineEdit(
            str(self.current)
        )

        layout.addWidget(
            self.path
        )



        self.search=QLineEdit()

        self.search.setPlaceholderText(
            "Search..."
        )

        self.search.textChanged.connect(
            self.refresh
        )


        layout.addWidget(
            self.search
        )



        row=QHBoxLayout()


        buttons=[
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

        layout.addWidget(
            self.list
        )



    def refresh(self):

        self.list.clear()

        key=self.search.text().lower()


        for item in self.current.iterdir():

            if key in item.name.lower():

                i=QListWidgetItem(
                    item.name
                )

                i.setData(
                    Qt.UserRole,
                    str(item)
                )

                self.list.addItem(i)





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

            if p.is_dir():

                shutil.rmtree(p)

            else:

                p.unlink()

            self.refresh()




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
            "MiniOS Settings"
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
            QLabel("MiniOS 1.0")
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

        self.wallpaper.setPlaceholderText(
            "Wallpaper path"
        )


        layout.addRow(
            "Wallpaper",
            self.wallpaper
        )



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

        self.state.theme_name = (
            self.theme.text()
        )


        self.state.wallpaper = (
            self.wallpaper.text()
        )


        self.state.save_preferences()


        QMessageBox.information(
            self,
            "Settings",
            "Settings Saved"
        )