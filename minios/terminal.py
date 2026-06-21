from __future__ import annotations

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QLabel,
    QApplication
)



class TerminalWindow(QWidget):

    def __init__(self,state,parent=None):

        super().__init__(parent)


        self.state = state


        self.setWindowTitle(
            "MiniOS Terminal"
        )


        self.resize(
            850,
            550
        )


        self.current_dir = (
            state.sandbox_root
        )


        self.history=[]



        self.build()



    def build(self):

        layout=QVBoxLayout(
            self
        )


        title=QLabel(
            "MiniOS Command Prompt"
        )


        title.setFont(
            QFont(
                "Consolas",
                16,
                QFont.Bold
            )
        )


        layout.addWidget(title)



        self.output=QTextEdit()

        self.output.setReadOnly(
            True
        )


        self.output.setFont(
            QFont(
                "Consolas",
                11
            )
        )


        layout.addWidget(
            self.output
        )



        self.input=QLineEdit()


        self.input.setFont(
            QFont(
                "Consolas",
                12
            )
        )


        self.input.returnPressed.connect(
            self.execute
        )


        layout.addWidget(
            self.input
        )



        self.print_line(
            "MiniOS Terminal Started"
        )

        self.print_line(
            "Type help for commands"
        )





    def print_line(self,text):

        self.output.append(
            str(text)
        )





    def execute(self):

        cmd=self.input.text().strip()

        self.input.clear()


        if cmd=="":

            return



        self.history.append(
            cmd
        )


        self.print_line(
            "> "+cmd
        )


        parts=cmd.split()

        command=parts[0].lower()



        try:



            # HELP

            if command=="help":

                self.print_line(
"""
Available Commands:

help
dir
ls
mkdir folder
cd folder
pwd
cls
time
date
echo text
shutdown
restart
logout

"""
                )



            # DIR

            elif command=="dir" or command=="ls":


                files=list(
                    self.current_dir.iterdir()
                )


                if not files:

                    self.print_line(
                        "Empty Directory"
                    )


                for f in files:

                    if f.is_dir():

                        self.print_line(
                            "[DIR] "+f.name
                        )

                    else:

                        self.print_line(
                            f.name
                        )




            # MKDIR

            elif command=="mkdir":


                if len(parts)<2:

                    self.print_line(
                        "Usage: mkdir foldername"
                    )

                else:

                    folder=(
                        self.current_dir
                        /
                        parts[1]
                    )


                    folder.mkdir(
                        exist_ok=True
                    )


                    self.print_line(
                        "Folder created"
                    )




            # CD

            elif command=="cd":


                if len(parts)<2:

                    self.print_line(
                        str(
                        self.current_dir
                        )
                    )


                else:

                    new=(
                        self.current_dir
                        /
                        parts[1]
                    )


                    if new.exists() and new.is_dir():

                        self.current_dir=new

                    else:

                        self.print_line(
                            "Folder not found"
                        )





            # PWD

            elif command=="pwd":

                self.print_line(
                    str(
                    self.current_dir
                    )
                )





            # CLEAR

            elif command=="cls":

                self.output.clear()





            # TIME

            elif command=="time":


                self.print_line(
                    datetime.now()
                    .strftime(
                    "%H:%M:%S"
                    )
                )





            # DATE

            elif command=="date":


                self.print_line(
                    datetime.now()
                    .strftime(
                    "%d-%m-%Y"
                    )
                )





            # ECHO


            elif command=="echo":


                self.print_line(
                    " ".join(
                    parts[1:]
                    )
                )

            # READ
            elif command == "read":
                if len(parts) < 2:
                    self.print_line("Usage: read filename")
                else:
                    target = self.current_dir / parts[1]
                    if target.exists() and target.is_file():
                        try:
                            content = target.read_text(encoding="utf-8")
                            self.print_line(content)
                        except Exception as e:
                            self.print_line(f"Error reading file: {e}")
                    else:
                        self.print_line("File not found")

            # WRITE
            elif command == "write":
                if len(parts) < 3:
                    self.print_line("Usage: write filename content...")
                else:
                    target = self.current_dir / parts[1]
                    content = " ".join(parts[2:])
                    try:
                        target.write_text(content, encoding="utf-8")
                        self.print_line(f"Successfully wrote to {parts[1]}")
                    except Exception as e:
                        self.print_line(f"Error writing to file: {e}")


            # SHUTDOWN


            elif command=="shutdown":

                QApplication.quit()





            # RESTART


            elif command=="restart":


                os.execl(
                    sys.executable,
                    sys.executable,
                    *sys.argv
                )





            # LOGOUT


            elif command=="logout":

                self.close()





            else:


                self.print_line(
                    "Command not found"
                )



        except Exception as e:


            self.print_line(
                "Error: "+str(e)
            )