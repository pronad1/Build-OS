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
        self.setWindowTitle("KALI Terminal")
        self.resize(850, 550)
        self.current_dir = state.sandbox_root
        self.history = []
        self.editor_mode = False
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

        title=QLabel("KALI Terminal - Professional Edition")
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

    def print_line(self, text):
        self.output.append(str(text))

    def execute(self):
        cmd = self.input.text().strip()
        self.input.clear()
        
        user = self.state.current_user or "user"

        if cmd == "":
            self.print_line(f"${user}> ")
            return

        self.history.append(cmd)
        self.print_line(f"${user}> " + cmd)

        parts = cmd.split()
        command = parts[0].lower()

        try:
            # HELP
            if command == "help":
                self.print_line(
"""Available Commands:
help
dir / ls
mkdir folder
cd folder
pwd
cls / clear
time
date
echo text
read filename
write filename text...
touch filename
nano filename
rm filename
apt install package
python script.py
shutdown
restart
logout""")

            # APT
            elif command == "apt":
                if len(parts) < 3 or parts[1] != "install":
                    self.print_line("Usage: apt install <package>")
                else:
                    pkg = parts[2]
                    self.print_line(f"Reading package lists... Done")
                    self.print_line(f"Building dependency tree... Done")
                    self.print_line(f"Installing {pkg}...")
                    if pkg == "nmap":
                        self.print_line("Unpacking nmap (7.93-1kali1) ...")
                        self.print_line("Setting up nmap...")
                        self.state.installed_apps = getattr(self.state, 'installed_apps', [])
                        if "nmap" not in self.state.installed_apps:
                            self.state.installed_apps.append("nmap")
                        self.print_line("Done.")
                    else:
                        self.print_line(f"E: Unable to locate package {pkg}")

            elif command == "nmap":
                if "nmap" in getattr(self.state, 'installed_apps', []):
                    self.print_line(f"Starting Nmap 7.93 ( https://nmap.org )")
                    self.print_line("Nmap scan report for " + (parts[1] if len(parts)>1 else "localhost"))
                    self.print_line("Host is up (0.00013s latency).")
                    self.print_line("Not shown: 999 closed ports")
                    self.print_line("PORT   STATE SERVICE\n22/tcp open  ssh")
                    self.print_line("\nNmap done: 1 IP address (1 host up) scanned in 0.14 seconds")
                else:
                    self.print_line("Command not found. Did you mean: apt install nmap?")

            # DIR
            elif command in ["dir", "ls"]:
                files = list(self.current_dir.iterdir())
                if not files:
                    self.print_line("Empty Directory")
                for f in files:
                    if f.is_dir():
                        self.print_line("[DIR] " + f.name)
                    else:
                        self.print_line(f.name)

            # MKDIR
            elif command == "mkdir":
                if len(parts) < 2:
                    self.print_line("Usage: mkdir foldername")
                else:
                    folder = self.current_dir / parts[1]
                    folder.mkdir(exist_ok=True)
                    self.print_line("Folder created")

            # CD
            elif command == "cd":
                if len(parts) < 2:
                    self.print_line(str(self.current_dir))
                else:
                    new = self.current_dir / parts[1]
                    if new.exists() and new.is_dir():
                        self.current_dir = new
                    else:
                        self.print_line("Folder not found")

            # PWD
            elif command == "pwd":
                self.print_line(str(self.current_dir))

            # CLEAR
            elif command in ["cls", "clear"]:
                self.output.clear()

            # TIME
            elif command == "time":
                self.print_line(datetime.now().strftime("%H:%M:%S"))

            # DATE
            elif command == "date":
                self.print_line(datetime.now().strftime("%d-%m-%Y"))

            # ECHO
            elif command == "echo":
                self.print_line(" ".join(parts[1:]))

            # READ
            elif command == "read":
                if len(parts) < 2:
                    self.print_line("Usage: read filename")
                else:
                    target = self.current_dir / parts[1]
                    if target.exists() and target.is_file():
                        self.print_line(target.read_text(encoding="utf-8"))
                    else:
                        self.print_line("File not found")

            # WRITE
            elif command == "write":
                if len(parts) < 3:
                    self.print_line("Usage: write filename content...")
                else:
                    target = self.current_dir / parts[1]
                    target.write_text(" ".join(parts[2:]), encoding="utf-8")
                    self.print_line(f"Successfully wrote to {parts[1]}")

            # TOUCH
            elif command == "touch":
                if len(parts) < 2:
                    self.print_line("Usage: touch filename")
                else:
                    target = self.current_dir / parts[1]
                    target.touch()
                    self.print_line(f"File created: {parts[1]}")

            # NANO
            elif command == "nano":
                if len(parts) < 2:
                    self.print_line("Usage: nano filename")
                else:
                    target = self.current_dir / parts[1]
                    if not target.exists():
                        target.touch()
                    self.nano_target = target
                    self.enter_nano_mode()

            # RM
            elif command == "rm":
                if len(parts) < 2:
                    self.print_line("Usage: rm filename")
                else:
                    target = self.current_dir / parts[1]
                    if target.exists():
                        recycle_bin = self.state.sandbox_root / "Recycle Bin"
                        recycle_bin.mkdir(exist_ok=True)
                        dest = recycle_bin / target.name
                        if dest.exists():
                            dest = recycle_bin / f"{target.name}_{datetime.now().strftime('%H%M%S')}"
                        shutil.move(str(target), str(dest))
                        self.print_line(f"Moved {parts[1]} to Recycle Bin")
                    else:
                        self.print_line("File not found")

            # PYTHON
            elif command == "python":
                if len(parts) < 2:
                    self.print_line("Usage: python script.py")
                else:
                    script_path = self.current_dir / parts[1]
                    if script_path.exists() and script_path.is_file():
                        self.print_line(f"Running {parts[1]}...")
                        import subprocess
                        result = subprocess.run(
                            [sys.executable, str(script_path)],
                            capture_output=True, text=True, timeout=10, cwd=str(self.current_dir)
                        )
                        if result.stdout:
                            self.print_line(result.stdout.strip())
                        if result.stderr:
                            self.print_line("Errors:\n" + result.stderr.strip())
                        self.print_line(f"Process exited with code {result.returncode}")
                    else:
                        self.print_line("Python script not found")

            # SHUTDOWN / LOGOUT / RESTART
            elif command == "shutdown":
                QApplication.quit()
            elif command == "restart":
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif command == "logout":
                self.close()
            else:
                self.print_line("Command not found")

        except Exception as e:
            self.print_line(f"Error: {e}")

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
        self.setWindowTitle(f"Nano: {self.nano_target.name} (Ctrl+S Save | Ctrl+Q Quit)")

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
        self.setWindowTitle("KALI Terminal")

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
