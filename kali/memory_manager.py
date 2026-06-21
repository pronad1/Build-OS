from __future__ import annotations

from dataclasses import dataclass

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QSpinBox,
    QListWidget,
    QListWidgetItem,
    QMessageBox
)

from .widgets import MemoryBarWidget



@dataclass
class ProcessMemory:

    name:str
    size:int




class MemoryManagerWindow(QWidget):


    def __init__(self,parent=None):

        super().__init__(parent)


        self.setWindowTitle(
            "Memory Manager"
        )

        self.resize(
            950,600
        )


        self.total_memory=1000


        self.processes=[]


        self.free_memory=self.total_memory


        self.build_ui()


        self.refresh()




    def build_ui(self):

        layout=QVBoxLayout(self)



        title=QLabel(
            "Memory Management"
        )

        title.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )


        layout.addWidget(title)




        info=QHBoxLayout()


        self.total_label=QLabel()

        self.used_label=QLabel()

        self.free_label=QLabel()


        info.addWidget(
            self.total_label
        )

        info.addWidget(
            self.used_label
        )

        info.addWidget(
            self.free_label
        )


        layout.addLayout(info)




        form=QHBoxLayout()


        self.name=QLineEdit()

        self.name.setPlaceholderText(
            "Process Name"
        )


        self.size=QSpinBox()

        self.size.setRange(
            10,500
        )

        self.size.setValue(
            100
        )



        self.algorithm=QComboBox()


        self.algorithm.addItems(
        [
            "First Fit",
            "Best Fit",
            "Worst Fit",
            "Paging"
        ])



        add=QPushButton(
            "Allocate"
        )

        add.clicked.connect(
            self.allocate
        )


        remove=QPushButton(
            "Remove"
        )

        remove.clicked.connect(
            self.remove
        )


        form.addWidget(self.name)

        form.addWidget(self.size)

        form.addWidget(self.algorithm)

        form.addWidget(add)

        form.addWidget(remove)



        layout.addLayout(form)





        self.bar=MemoryBarWidget()


        layout.addWidget(
            self.bar
        )




        self.list=QListWidget()

        layout.addWidget(
            self.list
        )






    def allocate(self):

        name=self.name.text()


        if name=="":
            name="Process"



        size=self.size.value()


        if size>self.free_memory:

            QMessageBox.warning(
                self,
                "Memory",
                "Not enough memory"
            )

            return




        mode=self.algorithm.currentText()



        if mode=="Paging":

            pages=size//50+1

            name += (
                f" ({pages} pages)"
            )




        self.processes.append(
            ProcessMemory(
                name,
                size
            )
        )


        self.free_memory-=size


        self.refresh()




    def remove(self):

        item=self.list.currentItem()


        if not item:
            return



        index=self.list.row(
            item
        )


        process=self.processes.pop(
            index
        )


        self.free_memory += (
            process.size
        )


        self.refresh()







    def refresh(self):


        used=sum(
            p.size
            for p in self.processes
        )


        self.total_label.setText(
            f"Total: {self.total_memory} MB"
        )


        self.used_label.setText(
            f"Used: {used} MB"
        )


        self.free_label.setText(
            f"Free: {self.free_memory} MB"
        )




        self.list.clear()



        colors=[
            "#22c55e",
            "#06b6d4",
            "#f97316",
            "#a855f7"
        ]



        partitions=[]



        for i,p in enumerate(self.processes):

            self.list.addItem(
                QListWidgetItem(
                    f"{p.name}  - {p.size} MB"
                )
            )


            partitions.append(
                (
                    p.name,
                    p.size,
                    QColor(
                    colors[i%len(colors)]
                    )
                )
            )



        if self.free_memory>0:

            partitions.append(
                (
                    "Free",
                    self.free_memory,
                    QColor("#334155")
                )
            )



        self.bar.set_partitions(
            partitions
        )