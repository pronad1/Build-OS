from kali.shell import run_app


if __name__ == "__main__":
    run_app()





# from __future__ import annotations

# import sys
# import os

# from pathlib import Path

# from PyQt5.QtCore import Qt, QTimer
# from PyQt5.QtGui import QFont
# from PyQt5.QtWidgets import (
#     QApplication,
#     QDialog,
#     QFrame,
#     QGridLayout,
#     QHBoxLayout,
#     QLabel,
#     QLineEdit,
#     QMainWindow,
#     QPushButton,
#     QVBoxLayout,
#     QWidget,
#     QMessageBox
# )


# from .modules import (
#     FileExplorerWindow,
#     NotepadWindow,
#     CalculatorWindow,
#     TaskManagerWindow,
#     SettingsWindow
# )

# from .memory_manager import MemoryManagerWindow
# from .scheduler import CpuSchedulerWindow
# from .state import MiniOSState



# # ================= LOGIN =================
# # ================= LOGIN =================

# class LoginDialog(QDialog):

#     def __init__(self,state,parent=None):

#         super().__init__(parent)

#         self.state=state

#         self.setWindowTitle(
#             "MiniOS Login"
#         )

#         self.resize(
#             800,
#             600
#         )


#         layout=QVBoxLayout(self)


#         title=QLabel("KALI")

#         title.setFont(
#             QFont(
#                 "Arial",
#                 36,
#                 QFont.Bold
#             )
#         )

#         title.setAlignment(
#             Qt.AlignCenter
#         )


#         layout.addWidget(title)



#         self.user=QLineEdit()

#         self.user.setMinimumHeight(45)

#         self.user.setPlaceholderText(
#             "Username"
#         )


#         self.password=QLineEdit()

#         self.password.setMinimumHeight(45)

#         self.password.setPlaceholderText(
#             "Password"
#         )


#         self.password.setEchoMode(
#             QLineEdit.Password
#         )


#         layout.addWidget(self.user)
#         layout.addWidget(self.password)



#         btn=QPushButton(
#             "LOGIN"
#         )


#         btn.setMinimumHeight(
#             45
#         )


#         btn.clicked.connect(
#             self.login
#         )


#         layout.addWidget(btn)



#         self.msg=QLabel()

#         self.msg.setAlignment(
#             Qt.AlignCenter
#         )


#         layout.addWidget(
#             self.msg
#         )



#     def login(self):

#         if self.state.authenticate(
#             self.user.text(),
#             self.password.text()
#         ):

#             self.state.current_user=self.user.text()

#             self.accept()

#         else:

#             self.msg.setText(
#                 "Wrong Username or Password"
#             )





# # ================= DESKTOP =================


# class DesktopLauncher(QMainWindow):


#     def __init__(self,state):

#         super().__init__()


#         self.state=state

#         self.windows={}


#         self.setWindowTitle(
#             "MiniOS Desktop"
#         )


#         self.resize(
#             1400,
#             850
#         )


#         self.build()





#     def build(self):


#         central=QWidget()

#         self.setCentralWidget(
#             central
#         )


#         root=QVBoxLayout(
#             central
#         )


#         desktop=QFrame()


#         layout=QVBoxLayout(
#             desktop
#         )



#         title=QLabel(
#             "Mini Operating System Simulator"
#         )


#         title.setFont(
#             QFont(
#                 "Arial",
#                 28,
#                 QFont.Bold
#             )
#         )


#         layout.addWidget(title)



#         self.grid=QGridLayout()



#         icons=[


#             ("📁 File Explorer",
#             self.open_file_explorer),


#             ("📝 Notepad",
#             self.open_notepad),


#             ("🧮 Calculator",
#             self.open_calculator),


#             ("📊 Task Manager",
#             self.open_task_manager),


#             ("🧠 Memory Manager",
#             self.open_memory_manager),


#             ("⚙ Settings",
#             self.open_settings),


#             ("📋 Scheduler",
#             self.open_scheduler),


#             ("💻 Terminal",
#             self.open_terminal)

#         ]




#         for i,(name,func) in enumerate(icons):


#             btn=QPushButton(name)


#             btn.setMinimumSize(
#                 180,
#                 100
#             )


#             btn.clicked.connect(
#                 func
#             )


#             self.grid.addWidget(
#                 btn,
#                 i//4,
#                 i%4
#             )



#         layout.addLayout(
#             self.grid
#         )



#         root.addWidget(
#             desktop
#         )



#         # Taskbar

#         taskbar=QFrame()


#         bar=QHBoxLayout(
#             taskbar
#         )


#         start=QPushButton(
#             "Start"
#         )


#         start.clicked.connect(
#             self.power_menu
#         )


#         bar.addWidget(start)


#         bar.addStretch()



#         self.clock=QLabel()

#         bar.addWidget(
#             self.clock
#         )


#         root.addWidget(
#             taskbar
#         )



#         self.timer=QTimer(self)

#         self.timer.timeout.connect(
#             self.update_clock
#         )


#         self.timer.start(
#             1000
#         )




#     def update_clock(self):

#         self.clock.setText(
#             QTimer().tr(
#             "MiniOS Running"
#             )
#         )




#     # ========== PROCESS LAUNCH ==========


#     def launch(self,key,obj,name):


#         if key in self.windows:

#             self.windows[key].show()

#             self.windows[key].raise_()

#             return



#         pid=self.state.start_process(
#             name,
#             "application"
#         )


#         self.state.bind_window(
#             pid,
#             obj
#         )



#         obj.setAttribute(
#             Qt.WA_DeleteOnClose
#         )


#         obj.destroyed.connect(
#             lambda:
#             self.state.unbind_window(pid)
#         )


#         self.windows[key]=obj


#         obj.show()




#     # ===== MODULES =====


#     def open_file_explorer(self):

#         self.launch(
#             "file",
#             FileExplorerWindow(self.state),
#             "FileExplorer.exe"
#         )



#     def open_notepad(self):

#         self.launch(
#             "notepad",
#             NotepadWindow(self.state),
#             "Notepad.exe"
#         )



#     def open_calculator(self):

#         self.launch(
#             "calculator",
#             CalculatorWindow(),
#             "Calculator.exe"
#         )



#     def open_task_manager(self):

#         self.launch(
#             "task",
#             TaskManagerWindow(self.state),
#             "TaskManager.exe"
#         )



#     def open_memory_manager(self):

#         self.launch(
#             "memory",
#             MemoryManagerWindow(),
#             "MemoryManager.exe"
#         )



#     def open_scheduler(self):

#         self.launch(
#             "scheduler",
#             CpuSchedulerWindow(),
#             "Scheduler.exe"
#         )



#     def open_settings(self):

#         self.launch(
#             "settings",
#             SettingsWindow(self.state),
#             "Settings.exe"
#         )



#     def open_terminal(self):

#         from .terminal import TerminalWindow


#         self.launch(
#             "terminal",
#             TerminalWindow(self.state),
#             "Terminal.exe"
#         )




#     # POWER


#     def power_menu(self):

#         msg=QMessageBox(self)

#         msg.setWindowTitle(
#             "Power"
#         )


#         shutdown=msg.addButton(
#             "Shutdown",
#             QMessageBox.AcceptRole
#         )


#         restart=msg.addButton(
#             "Restart",
#             QMessageBox.AcceptRole
#         )


#         logout=msg.addButton(
#             "Logout",
#             QMessageBox.AcceptRole
#         )


#         msg.exec_()



#         if msg.clickedButton()==shutdown:

#             QApplication.quit()



#         elif msg.clickedButton()==restart:

#             os.execl(
#                 sys.executable,
#                 sys.executable,
#                 *sys.argv
#             )



#         elif msg.clickedButton()==logout:

#             self.close()





# # ================= RUN =================


# def run_app():


#     app=QApplication([])


#     state=MiniOSState(
#         Path(__file__).resolve().parents[1]
#     )


#     state.load_preferences()



#     login=LoginDialog(
#         state
#     )


#     if login.exec_()!=QDialog.Accepted:

#         return



#     desktop=DesktopLauncher(
#         state
#     )


#     desktop.show()


#     app.exec_()