from __future__ import annotations

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QLabel,
    QApplication,
    QShortcut
)



class TerminalWindow(QWidget):

    def __init__(self,state,parent=None):

        super().__init__(parent)


        self.state = state


        self.setWindowTitle(
            "KALI Terminal"
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

        self.setStyleSheet("""
            QWidget {
                background-color: #1a1c23;
                color: #e0e0e0;
            }
            QTextEdit {
                background-color: #1a1c23;
                color: #e0e0e0;
                border: none;
                padding: 10px;
                selection-background-color: #35bf5c;
            }
            QLineEdit {
                background-color: #1a1c23;
                color: #e0e0e0;
                border: none;
                padding: 5px 0px;
                selection-background-color: #35bf5c;
            }
        """)

        layout=QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)

        title=QLabel("KALI Terminal - Manjaro Edition")
        title.setFont(QFont("Consolas", 12, QFont.Bold))
        title.setStyleSheet("color: #35bf5c; padding: 5px;")
        layout.addWidget(title)

        self.output=QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 11))
        layout.addWidget(self.output)

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(10, 0, 10, 10)
        
        user = self.state.current_user or "user"
        self.prompt_label = QLabel(f"${user}>")
        self.prompt_label.setFont(QFont("Consolas", 12, QFont.Bold))
        self.prompt_label.setStyleSheet("color: #35bf5c;")
        input_layout.addWidget(self.prompt_label)

        self.input=QLineEdit()
        self.input.setFont(QFont("Consolas", 12))
        self.input.returnPressed.connect(self.execute)
        input_layout.addWidget(self.input)

        layout.addLayout(input_layout)

        self.shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut_save.activated.connect(self.nano_save)
        self.shortcut_save.setEnabled(False)

        self.shortcut_quit = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.shortcut_quit.activated.connect(self.nano_quit)
        self.shortcut_quit.setEnabled(False)

        self.print_line("KALI Terminal Started")
        self.print_line("Type help for commands")





    def print_line(self,text):

        self.output.append(
            str(text)
        )





    def execute(self):

        cmd=self.input.text().strip()
        self.input.clear()
        
        user = self.state.current_user or "user"

        if cmd=="":
            self.print_line(f"${user}> ")
            return

        self.history.append(cmd)

        self.print_line(f"${user}> " + cmd)


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
read filename
write filename text...
touch filename
nano filename
rm filename
python script.py
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

            # TOUCH (CREATE)
            elif command == "touch":
                if len(parts) < 2:
                    self.print_line("Usage: touch filename")
                else:
                    target = self.current_dir / parts[1]
                    try:
                        target.touch()
                        self.print_line(f"File created: {parts[1]}")
                    except Exception as e:
                        self.print_line(f"Error creating file: {e}")

            # NANO
            elif command == "nano":
                if len(parts) < 2:
                    self.print_line("Usage: nano filename")
                else:
                    target = self.current_dir / parts[1]
                    try:
                        if not target.exists():
                            target.touch()
                        self.nano_target = target
                        self.enter_nano_mode()
                    except Exception as e:
                        self.print_line(f"Error opening/creating file: {e}")

            # RM (DELETE)
            elif command == "rm":
                if len(parts) < 2:
                    self.print_line("Usage: rm filename")
                else:
                    target = self.current_dir / parts[1]
                    if target.exists():
                        try:
                            recycle_bin = self.state.sandbox_root / "Recycle Bin"
                            recycle_bin.mkdir(exist_ok=True)
                            dest = recycle_bin / target.name
                            if dest.exists():
                                dest = recycle_bin / f"{target.name}_{datetime.now().strftime('%H%M%S')}"
                            shutil.move(str(target), str(dest))
                            self.print_line(f"Moved {parts[1]} to Recycle Bin")
                        except Exception as e:
                            self.print_line(f"Error deleting file: {e}")
                    else:
                        self.print_line("File not found")

            # PYTHON
            elif command == "python":
                if len(parts) < 2:
                    self.print_line("Usage: python script.py")
                else:
                    script_path = self.current_dir / parts[1]
                    if script_path.exists() and script_path.is_file():
                        try:
                            self.print_line(f"Running {parts[1]}...")
                            import subprocess
                            result = subprocess.run(
                                [sys.executable, str(script_path)],
                                capture_output=True,
                                text=True,
                                timeout=10,
                                cwd=str(self.current_dir)
                            )
                            if result.stdout:
                                self.print_line(result.stdout.strip())
                            if result.stderr:
                                self.print_line("Errors:\\n" + result.stderr.strip())
                            self.print_line(f"Process exited with code {result.returncode}")
                        except subprocess.TimeoutExpired:
                            self.print_line("Error: Script timed out after 10 seconds.")
                        except Exception as e:
                            self.print_line(f"Error executing python: {e}")
                    else:
                        self.print_line("Python script not found")



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

    def enter_nano_mode(self):
        self.editor_mode = True
        self.terminal_history_text = self.output.toHtml()
        
        self.output.clear()
        self.output.setPlainText(self.nano_target.read_text(encoding="utf-8"))
        self.output.setReadOnly(False)
        self.output.setFocus()
        
        self.prompt_label.setText("Nano Editor:")
        self.input.setText("Ctrl+S: Save & Exit | Ctrl+Q: Quit without saving")
        self.input.setReadOnly(True)
        
        self.shortcut_save.setEnabled(True)
        self.shortcut_quit.setEnabled(True)

    def exit_nano_mode(self):
        self.editor_mode = False
        self.output.setReadOnly(True)
        self.output.setHtml(self.terminal_history_text)
        
        user = self.state.current_user or "user"
        self.prompt_label.setText(f"${user}>")
        self.input.setReadOnly(False)
        self.input.clear()
        self.input.setFocus()
        
        self.shortcut_save.setEnabled(False)
        self.shortcut_quit.setEnabled(False)

    def nano_save(self):
        if getattr(self, 'editor_mode', False) and getattr(self, 'nano_target', None):
            try:
                self.nano_target.write_text(self.output.toPlainText(), encoding="utf-8")
            except Exception as e:
                pass
            self.exit_nano_mode()
            self.print_line(f"Saved {self.nano_target.name}")

    def nano_quit(self):
        if getattr(self, 'editor_mode', False):
            self.exit_nano_mode()