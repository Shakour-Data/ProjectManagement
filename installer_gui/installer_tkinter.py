import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import platform
import datetime

class InstallerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ProjectManagement Installer")
        self.geometry("600x450")
        self.resizable(False, False)

        self.log_file_path = "installer_log.txt"
        self.create_widgets()
        self.log("Installer started.")

        self.backend_process = None
        self.frontend_process = None

    def create_widgets(self):
        self.label = ttk.Label(self, text="ProjectManagement Installation Progress", font=("Arial", 14))
        self.label.pack(pady=10)

        self.progress = ttk.Progressbar(self, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=10)

        self.log_text = tk.Text(self, height=18, width=70, state="disabled")
        self.log_text.pack(pady=10)

        self.install_button = ttk.Button(self, text="Start Installation", command=self.start_installation)
        self.install_button.pack(pady=10)

        self.verify_comm_button = ttk.Button(self, text="Verify Backend-Frontend Communication", command=self.verify_backend_frontend_communication)
        self.verify_comm_button.pack(pady=10)

        self.stop_backend_button = ttk.Button(self, text="Stop Backend Server", command=self.stop_backend_server, state="disabled")
        self.stop_backend_button.pack(pady=5)

        self.start_backend_button = ttk.Button(self, text="Start Backend Server", command=self.start_backend_server)
        self.start_backend_button.pack(pady=5)

        self.stop_frontend_button = ttk.Button(self, text="Stop Frontend Server", command=self.stop_frontend_server, state="disabled")
        self.stop_frontend_button.pack(pady=5)

        self.start_frontend_button = ttk.Button(self, text="Start Frontend Server", command=self.start_frontend_server)
        self.start_frontend_button.pack(pady=5)

        self.instructions_label = ttk.Label(self, text="Access the frontend UI at http://localhost:3000\nUse the buttons above to start/stop the servers.", font=("Arial", 10))
        self.instructions_label.pack(pady=10)

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, full_message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        with open(self.log_file_path, "a", encoding="utf-8") as f:
            f.write(full_message + "\n")

    def start_installation(self):
        self.install_button.config(state="disabled")
        threading.Thread(target=self.run_installation).start()

    def run_installation(self):
        try:
            self.log("Starting installation process...")
            self.update_progress(0)

            self.log("Creating virtual environment...")
            self.update_progress(10)
            self.create_virtualenv()

            self.log("Installing Python dependencies...")
            self.update_progress(30)
            self.install_python_dependencies()

            self.log("Installing Node.js dependencies and building frontend...")
            self.update_progress(60)
            self.install_node_dependencies()

            self.log("Starting backend server...")
            self.update_progress(80)
            self.start_backend_server()

            self.log("Starting frontend server...")
            self.start_frontend_server()

            self.stop_backend_button.config(state="normal")
            self.stop_frontend_button.config(state="normal")

            self.log("Installation and startup complete.")
            self.update_progress(100)
            messagebox.showinfo("Installation", "ProjectManagement installation and startup completed successfully.")
        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Installation Error", str(e))
        finally:
            self.install_button.config(state="normal")

    def start_backend_server(self):
        if self.backend_process and self.backend_process.poll() is None:
            self.log("Backend server is already running.")
            return
        backend_cmd = self.get_backend_command()
        self.backend_process = subprocess.Popen(backend_cmd)
        self.log("Backend server started on http://localhost:5050")

    def start_frontend_server(self):
        if self.frontend_process and self.frontend_process.poll() is None:
            self.log("Frontend server is already running.")
            return
        frontend_dir = os.path.join(os.getcwd(), "frontend")
        frontend_cmd = ["npm", "start"]
        self.frontend_process = subprocess.Popen(frontend_cmd, cwd=frontend_dir)
        self.log("Frontend server started on http://localhost:3000")

    def verify_backend_frontend_communication(self):
        import requests
        try:
            backend_url = "http://localhost:5050/health"
            frontend_url = "http://localhost:3000"
            backend_response = requests.get(backend_url, timeout=5)
            frontend_response = requests.get(frontend_url, timeout=5)
            if backend_response.status_code == 200 and frontend_response.status_code == 200:
                self.log("Backend and frontend communication verified successfully.")
                messagebox.showinfo("Verification", "Backend and frontend communication is working correctly.")
            else:
                self.log("Backend or frontend communication failed.")
                messagebox.showwarning("Verification", "Backend or frontend communication failed.")
        except Exception as e:
            self.log(f"Communication verification error: {e}")
            messagebox.showerror("Verification Error", str(e))

    def stop_backend_server(self):
        if self.backend_process and self.backend_process.poll() is None:
            self.backend_process.terminate()
            self.backend_process.wait()
            self.log("Backend server stopped.")
            self.stop_backend_button.config(state="disabled")
        else:
            self.log("Backend server is not running.")

    def stop_frontend_server(self):
        if self.frontend_process and self.frontend_process.poll() is None:
            self.frontend_process.terminate()
            self.frontend_process.wait()
            self.log("Frontend server stopped.")
            self.stop_frontend_button.config(state="disabled")
        else:
            self.log("Frontend server is not running.")

    def update_progress(self, value):
        self.progress['value'] = value
        self.update_idletasks()

    def create_virtualenv(self):
        if not os.path.exists("venv"):
            self.log("Creating virtual environment directory 'venv'...")
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
            self.log("Virtual environment created.")
        else:
            self.log("Virtual environment already exists.")

    def install_python_dependencies(self):
        pip_executable = self.get_pip_executable()
        self.log(f"Using pip executable: {pip_executable}")
        subprocess.check_call([pip_executable, "install", "-r", "requirements.txt"])

    def install_node_dependencies(self):
        frontend_dir = os.path.join(os.getcwd(), "frontend")
        if not os.path.exists(frontend_dir):
            raise FileNotFoundError("Frontend directory not found.")
        self.log("Installing npm packages...")
        subprocess.check_call(["npm", "install"], cwd=frontend_dir)
        self.log("Building frontend assets...")
        subprocess.check_call(["npm", "run", "build"], cwd=frontend_dir)

    def get_pip_executable(self):
        if platform.system() == "Windows":
            return os.path.join("venv", "Scripts", "pip.exe")
        else:
            return os.path.join("venv", "bin", "pip")

    def get_backend_command(self):
        if platform.system() == "Windows":
            uvicorn_path = os.path.join("venv", "Scripts", "uvicorn.exe")
        else:
            uvicorn_path = os.path.join("venv", "bin", "uvicorn")
        return [uvicorn_path, "backend.api:app", "--host", "0.0.0.0", "--port", "5050"]

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()
