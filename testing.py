import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QFileDialog, QTextEdit, QMenu, QSystemTrayIcon
from PyQt5.QtGui import QIcon, QFont
import subprocess
from PyQt5.QtCore import QSettings, QTimer, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IDE Hotkey System")
        self.setMinimumSize(400, 300)  # Set minimum size to prevent small resizing

        self.create_menu()
        self.setup_ui()

        # Load the last selected color mode
        settings = QSettings("MyCompany", "IDEHotkeySystem")
        last_mode = settings.value("color_mode", defaultValue="light")
        if last_mode == "light":
            self.set_color_mode("light")
        elif last_mode == "dark":
            self.set_color_mode("dark")

    # desktop tray icon (not functioning atm)
    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("IDE_icon.jpg"))
        self.tray_icon.setToolTip("IDE Hotkeys")
        self.tray_icon.activated.connect(self.tray_icon_activated)

    # open from the sys tray
    def tray_icon_activated(self,reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
        
    # create the menu at the top of the window for file/help menus
    def create_menu(self):
        main_menu = self.menuBar()

        file_menu = main_menu.addMenu("File")
        help_menu = main_menu.addMenu("Help")

        # help menu ui
        instructions_action = QAction("Instructions",self)
        instructions_action.triggered.connect(self.show_instructions)
        help_menu.addAction(instructions_action)

        # inside of the File menu, shows the Create Script functionality.
        create_script_action = QAction("Create Script", self)
        create_script_action.triggered.connect(self.create_script)
        file_menu.addAction(create_script_action)

        # inside of the File menu, shows the Load Script functionality.
        load_script_action = QAction("Load Script", self)
        load_script_action.triggered.connect(self.load_script)
        file_menu.addAction(load_script_action)

    def show_instructions(self):
        instructions_text = (
            "Instructions:\n\n"
            "1. Create a script by clicking the 'Create Script' button.\n"
            "2. Load a script by clicking the 'Load Script' button.\n"
            "3. Change the color mode using the mode selector button.\n\n"
        )
        if instructions_text:
            self.show_message_box("Instructions", instructions_text)
        else:
            QMessageBox.warning(self, "Instructions", "No instructions available.")


    def show_message_box(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        text_edit = QTextEdit()
        text_edit.setPlainText(message)
        text_edit.setReadOnly(True)
        text_edit.setMinimumSize(400, 300)  # Set minimum size for the QTextEdit widget
        msg_box.layout().addWidget(text_edit)
        msg_box.exec()


    def load_script(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Script", "", "Text files (*.txt);;All files (*)")
        if file_path:
            QMessageBox.information(self, "Load Script", f"File selected: {file_path}")

    def create_script(self):
        try:
            # Open Notepad
            process = subprocess.Popen(['notepad.exe'])
            
            # Disable UI
            self.disable_ui()

            # Check if Notepad is closed periodically
            timer = QTimer(self)
            timer.timeout.connect(lambda: self.check_notepad(process, timer))
            timer.start(1000)  # Check every second
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def disable_ui(self):
        # Disable all UI elements
        for widget in self.findChildren(QWidget):
            widget.setEnabled(False)

    def enable_ui(self):
        # Enable all UI elements
        for widget in self.findChildren(QWidget):
            widget.setEnabled(True)

    def check_notepad(self, process, timer):
        if process.poll() is not None:  # Notepad is closed
            timer.stop()  # Stop the timer
            self.enable_ui()  # Enable UI
            QTimer.singleShot(0, lambda: self.exec_main_progs())

    def exec_main_progs(self):
        # Execute programs !
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dummy_script_path = os.path.join(current_dir, "dummy.py")
            subprocess.run(["python", dummy_script_path])
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        title_label = QLabel("Welcome to the IDE Hotkey System")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = title_label.font()
        title_font.setPointSize(24)  # Adjust the font size
        title_font.setWeight(QFont.Bold)  # Make the font bold
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        create_script_button = QPushButton("Create Script")
        create_script_button.clicked.connect(self.create_script)
        layout.addWidget(create_script_button, alignment=Qt.AlignCenter)

        load_script_button = QPushButton("Load Script")
        load_script_button.clicked.connect(self.load_script)
        layout.addWidget(load_script_button, alignment=Qt.AlignCenter)

        self.color_mode_button = QPushButton("Light Mode")  # Initially set to Light Mode
        self.color_mode_button.clicked.connect(self.toggle_color_mode)
        layout.addWidget(self.color_mode_button, alignment=Qt.AlignCenter)

        # Initially set the flag to False (Light Mode)
        self.dark_mode_enabled = False

    def set_color_mode(self, mode):
        settings = QSettings("MyCompany", "IDEHotkeySystem")
        settings.setValue("color_mode", mode)

        if mode == "light":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f0f0f0;
                    color: #000;
                }
                QPushButton {
                    background-color: #dddddd;
                    color: #000;
                    border-radius: 5px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #cccccc;
                }
                QLabel {
                    color: #000;
                }
            """)
            self.color_mode_button.setText("Dark Mode")
        elif mode == "dark":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #222;
                    color: #fff;
                }
                QPushButton {
                    background-color: #444;
                    color: #fff;
                    border-radius: 5px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
                QLabel {
                    color: #fff;
                }
            """)
            self.color_mode_button.setText("Light Mode")

    def toggle_color_mode(self):
        # Toggle the flag
        self.dark_mode_enabled = not self.dark_mode_enabled
        # Update the color mode based on the flag
        new_mode = "dark" if self.dark_mode_enabled else "light"
        self.set_color_mode(new_mode)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
