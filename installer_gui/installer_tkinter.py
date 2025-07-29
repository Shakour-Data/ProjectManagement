import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox

class InstallerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ProjectManagement Installer")
        self.geometry("600x400")
        self.resizable(False, False)

        self.create_widgets()
        self.log("Installer started.")

    def create_widgets(self):
        self.label = ttk.Label(self, text="ProjectManagement Installation Progress", font=("Arial", 14))
        self.label.pack(pady=10)

        self.progress = ttk.Progressbar(self, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=10)

        self.log_text = tk.Text(self, height=15, width=70, state="disabled")
        self.log_text.pack(pady=10)

        self.install_button = ttk.Button(self, text="Start Installation", command=self.start_installation)
        self.install_button.pack(pady=10)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def start_installation(self):
        self.install_button.config(state="disabled")
        threading.Thread(target=self.run_installation).start()

    def run_installation(self):
        try:
            self.log("Creating virtual environment...")
            self.update_progress(10)
            self.create_virtualenv()

            self.log("Installing Python dependencies...")
            self.update_progress(30)
            self.install_python_dependencies()

            self.log("Installing Node.js dependencies and building frontend...")
            self.update_progress(60)
            self.install_node_dependencies()

            self.log("Installation complete.")
            self.update_progress(100)
            messagebox.showinfo("Installation", "ProjectManagement installation completed successfully.")
        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Installation Error", str(e))
        finally:
            self.install_button.config(state="normal")

    def update_progress(self, value):
        self.progress['value'] = value
        self.update_idletasks()

    def create_virtualenv(self):
        if not os.path.exists("venv"):
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        else:
            self.log("Virtual environment already exists.")

    def install_python_dependencies(self):
        pip_executable = os.path.join("venv", "bin", "pip")
        subprocess.check_call([pip_executable, "install", "-r", "requirements.txt"])

    def install_node_dependencies(self):
        frontend_dir = os.path.join(os.getcwd(), "frontend")
        if not os.path.exists(frontend_dir):
            raise FileNotFoundError("Frontend directory not found.")
        # Install npm packages
        subprocess.check_call(["npm", "install"], cwd=frontend_dir)
        # Build frontend assets
        subprocess.check_call(["npm", "run", "build"], cwd=frontend_dir)

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()
