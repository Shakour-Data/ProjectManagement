import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWebChannel import QWebChannel
import threading
import time
import subprocess
import os
import platform

# Import the setup functions from cross_platform_setup.py
import cross_platform_setup

import json

class InstallerBackend(QObject):
    updateStatus = pyqtSignal(str)
    installationOptionSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.base_path = os.getcwd()
        self.installation_info_path = os.path.join(self.base_path, "installation_info.json")

    def check_existing_installation(self):
        if os.path.exists(self.installation_info_path):
            try:
                with open(self.installation_info_path, "r") as f:
                    info = json.load(f)
                version = info.get("version", "unknown")
                return True, version
            except Exception:
                return True, "unknown"
        return False, None

    @pyqtSlot(str)
    def handleInstallationOption(self, option):
        # option can be 'upgrade', 'repair', 'uninstall', 'fresh_install'
        self.installationOptionSelected.emit(option)
        if option == "upgrade":
            self.updateStatus.emit("Upgrading existing installation...")
            self.perform_upgrade()
        elif option == "repair":
            self.updateStatus.emit("Repairing existing installation...")
            self.perform_repair()
        elif option == "uninstall":
            self.updateStatus.emit("Uninstalling existing installation...")
            self.perform_uninstall()
        elif option == "fresh_install":
            self.updateStatus.emit("Performing fresh installation...")
            self.startInstallation()
        else:
            self.updateStatus.emit("Unknown installation option selected.")

    def perform_upgrade(self):
        # Implement upgrade logic here, e.g., backup data, update files
        self.updateStatus.emit("Backup existing data...")
        # Backup logic (simplified)
        backup_path = os.path.join(self.base_path, "backup_" + time.strftime("%Y%m%d_%H%M%S"))
        try:
            if not os.path.exists(backup_path):
                os.makedirs(backup_path)
            # Copy user data or config files to backup_path
            # For example:
            user_data_path = os.path.join(self.base_path, "user_data")
            if os.path.exists(user_data_path):
                import shutil
                shutil.copytree(user_data_path, os.path.join(backup_path, "user_data"))
            self.updateStatus.emit("Backup complete. Proceeding with upgrade...")
        except Exception as e:
            self.updateStatus.emit(f"Backup failed: {e}")
            return

        # Continue with installation steps (reuse startInstallation logic)
        self.startInstallation()

    def perform_repair(self):
        # Implement repair logic here
        self.updateStatus.emit("Repairing installation...")
        # For now, just run installation steps again
        self.startInstallation()

    def perform_uninstall(self):
        # Implement uninstall logic here
        self.updateStatus.emit("Uninstalling software...")
        try:
            import shutil
            if os.path.exists(self.base_path):
                shutil.rmtree(self.base_path)
            self.updateStatus.emit("Uninstallation complete.")
        except Exception as e:
            self.updateStatus.emit(f"Uninstallation failed: {e}")

    @pyqtSlot()
    def startInstallation(self):
        def run_installation():
            self.updateStatus.emit("Starting installation...")
            time.sleep(1)

            # Check and install Python if needed
            if not cross_platform_setup.check_command_exists("python") and not cross_platform_setup.check_command_exists("python3"):
                self.updateStatus.emit("Installing Python...")
                cross_platform_setup.install_python()
            else:
                self.updateStatus.emit("Python found.")

            time.sleep(1)

            # Check and install Node.js if needed
            if not cross_platform_setup.check_command_exists("node"):
                self.updateStatus.emit("Installing Node.js...")
                cross_platform_setup.install_node()
                if not cross_platform_setup.check_command_exists("node"):
                    self.updateStatus.emit("Node.js installation failed.")
                    return
            else:
                self.updateStatus.emit("Node.js found.")

            time.sleep(1)

            # Check and install Git if needed
            if not cross_platform_setup.check_command_exists("git"):
                self.updateStatus.emit("Installing Git...")
                cross_platform_setup.install_git()
                if not cross_platform_setup.check_command_exists("git"):
                    self.updateStatus.emit("Git installation failed.")
                    return
            else:
                self.updateStatus.emit("Git found.")

            time.sleep(1)

            # Ask user to select installation directory
            self.updateStatus.emit("Please select installation directory.")
            # Since GUI is in web view, directory selection should be handled in UI or fallback to default
            base_path = self.base_path

            # Create virtual environment
            self.updateStatus.emit("Creating virtual environment...")
            cross_platform_setup.create_virtualenv(os.path.join(base_path, "venv"))

            # Determine python executable in venv
            if platform.system() == "Windows":
                venv_python = os.path.join(base_path, "venv", "Scripts", "python.exe")
            else:
                venv_python = os.path.join(base_path, "venv", "bin", "python")

            # Install Python dependencies
            self.updateStatus.emit("Installing Python dependencies...")
            cross_platform_setup.install_python_dependencies(venv_python)

            # Install frontend dependencies if node exists
            if cross_platform_setup.check_command_exists("node"):
                self.updateStatus.emit("Installing frontend dependencies...")
                cross_platform_setup.install_frontend_dependencies(base_path)

            # Start backend server
            self.updateStatus.emit("Starting backend server...")
            backend_process = cross_platform_setup.start_backend_server(venv_python, base_path)
            time.sleep(5)

            # Start frontend server
            self.updateStatus.emit("Starting frontend server...")
            frontend_process = cross_platform_setup.start_frontend_server(base_path)
            time.sleep(5)

            # Open browser
            self.updateStatus.emit("Opening frontend UI in browser...")
            cross_platform_setup.open_browser()

            # Create desktop shortcut
            self.updateStatus.emit("Creating desktop shortcut...")
            cross_platform_setup.create_desktop_shortcut(base_path)

            # Save installation info
            try:
                info = {"version": "1.0.0", "install_date": time.strftime("%Y-%m-%d %H:%M:%S")}
                with open(self.installation_info_path, "w") as f:
                    json.dump(info, f)
            except Exception as e:
                self.updateStatus.emit(f"Failed to save installation info: {e}")

            self.updateStatus.emit("Installation complete!")

        threading.Thread(target=run_installation).start()

class InstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Management Installer")
        self.setGeometry(100, 100, 800, 600)

        self.web_view = QWebEngineView()
        self.web_view.load(QUrl.fromLocalFile(os.path.abspath("installer_gui/ui/index.html")))

        self.channel = QWebChannel()
        self.backend = InstallerBackend()
        self.channel.registerObject("backend", self.backend)
        self.web_view.page().setWebChannel(self.channel)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

def main():
    app = QApplication(sys.argv)
    window = InstallerWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
