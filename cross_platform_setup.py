import os
import sys
import subprocess
import platform
import shutil
import time
import tkinter as tk
from tkinter import filedialog, messagebox

def run_command(command, shell=False, cwd=None):
    print(f"Running command: {command}")
    if cwd:
        if shell:
            command = f"cd {cwd} && {command}" if isinstance(command, str) else command
        else:
            # If command is list, no need to prepend cd, just set cwd in subprocess.run
            pass
    result = subprocess.run(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd if not shell else None)
    if result.returncode != 0:
        print(f"Error running command: {result.stderr}")
        sys.exit(1)
    else:
        print(result.stdout)

def create_virtualenv(venv_path):
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
    else:
        print("Virtual environment already exists.")

def activate_virtualenv(venv_path):
    if platform.system() == "Windows":
        activate_script = os.path.join(venv_path, "Scripts", "activate")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")
    return activate_script

def install_python_dependencies(venv_python):
    print("Installing Python dependencies...")
    run_command([venv_python, "-m", "pip", "install", "--upgrade", "pip"])
    run_command([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])

def install_frontend_dependencies(base_path):
    print("Installing frontend dependencies...")
    frontend_path = os.path.join(base_path, "frontend")
    if not os.path.exists(frontend_path):
        print("Frontend directory not found!")
        sys.exit(1)
    run_command("npm install", shell=True, cwd=frontend_path)

def start_backend_server(venv_python, base_path):
    print("Starting backend server...")
    # Use subprocess.Popen to run in background
    backend_cmd = [venv_python, "-m", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
    backend_process = subprocess.Popen(backend_cmd, cwd=base_path)
    return backend_process

def start_frontend_server(base_path):
    print("Starting frontend server...")
    frontend_path = os.path.join(base_path, "frontend")
    frontend_process = subprocess.Popen(["npm", "start"], cwd=frontend_path, shell=True)
    return frontend_process

def open_browser():
    url = "http://localhost:3000"
    print(f"Opening browser at {url}...")
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(url)
        elif system == "Darwin":
            subprocess.Popen(["open", url])
        else:
            subprocess.Popen(["xdg-open", url])
    except Exception as e:
        print(f"Failed to open browser: {e}")

def create_desktop_shortcut(base_path):
    system = platform.system()
    home = os.path.expanduser("~")
    desktop = ""
    shortcut_name = "ProjectManagement"

    if system == "Windows":
        desktop = os.path.join(home, "Desktop")
        shortcut_path = os.path.join(desktop, f"{shortcut_name}.lnk")
        try:
            # Import pywin32 modules only on Windows platform
            try:
                import importlib
                pythoncom = importlib.import_module('pythoncom')
                shell = importlib.import_module('win32com.shell.shell')
                shellcon = importlib.import_module('win32com.shell.shellcon')
                win32com_client = importlib.import_module('win32com.client')
                Dispatch = win32com_client.Dispatch
            except ImportError:
                print("pywin32 is required to create Windows shortcuts. Please install it manually using 'pip install pywin32'.")
                return

            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            # Target is python executable with this script
            python_exe = os.path.join(base_path, "venv", "Scripts", "python.exe")
            script_path = os.path.join(base_path, "cross_platform_setup.py")
            shortcut.Targetpath = python_exe
            shortcut.Arguments = f'"{script_path}"'
            shortcut.WorkingDirectory = base_path
            shortcut.IconLocation = python_exe
            shortcut.save()
            print(f"Desktop shortcut created at {shortcut_path}")
        except Exception as e:
            print(f"Failed to create Windows shortcut: {e}")

    elif system == "Darwin":
        desktop = os.path.join(home, "Desktop")
        shortcut_path = os.path.join(desktop, f"{shortcut_name}.command")
        try:
            with open(shortcut_path, "w") as f:
                f.write(f"#!/bin/bash\n")
                f.write(f"cd {base_path}\n")
                f.write(f"python3 cross_platform_setup.py\n")
            os.chmod(shortcut_path, 0o755)
            print(f"Desktop shortcut created at {shortcut_path}")
        except Exception as e:
            print(f"Failed to create macOS shortcut: {e}")

    else:  # Linux
        desktop = os.path.join(home, "Desktop")
        shortcut_path = os.path.join(desktop, f"{shortcut_name}.desktop")
        try:
            with open(shortcut_path, "w") as f:
                f.write("[Desktop Entry]\n")
                f.write(f"Name={shortcut_name}\n")
                f.write(f"Exec=python3 {os.path.join(base_path, 'cross_platform_setup.py')}\n")
                f.write("Type=Application\n")
                f.write("Terminal=true\n")
                f.write(f"Icon=utilities-terminal\n")
                f.write("Categories=Utility;\n")
            os.chmod(shortcut_path, 0o755)
            print(f"Desktop shortcut created at {shortcut_path}")
        except Exception as e:
            print(f"Failed to create Linux shortcut: {e}")

def check_command_exists(command):
    from shutil import which
    return which(command) is not None

import tkinter.messagebox as messagebox

import os
import platform

def check_default_python():
    if platform.system() == "Windows":
        possible_paths = [
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Python", "Python39", "python.exe"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Python", "Python310", "python.exe"),
            os.path.join(os.environ.get("PROGRAMFILES", ""), "Python39", "python.exe"),
            os.path.join(os.environ.get("PROGRAMFILES", ""), "Python310", "python.exe"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
    else:
        # For Unix-like systems, check common python3 path
        if shutil.which("python3"):
            return shutil.which("python3")
    return None

def check_default_node():
    if platform.system() == "Windows":
        possible_paths = [
            os.path.join(os.environ.get("ProgramFiles", ""), "nodejs", "node.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "nodejs", "node.exe"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
    else:
        if shutil.which("node"):
            return shutil.which("node")
    return None

def check_default_git():
    if platform.system() == "Windows":
        possible_paths = [
            os.path.join(os.environ.get("ProgramFiles", ""), "Git", "bin", "git.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Git", "bin", "git.exe"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
    else:
        if shutil.which("git"):
            return shutil.which("git")
    return None

def install_python():
    python_path = check_default_python()
    if python_path:
        print(f"Found Python at {python_path}")
    else:
        messagebox.showerror("Python Not Found", "Python is not installed in the default locations. Please install Python manually from https://www.python.org/downloads/")
        sys.exit(1)

def install_node():
    node_path = check_default_node()
    if node_path:
        print(f"Found Node.js at {node_path}")
    else:
        messagebox.showwarning("Node.js Not Found", "Node.js is not installed in the default locations. Please select the Node.js installation directory.")
        root = tk.Tk()
        root.withdraw()
        while True:
            selected_dir = filedialog.askdirectory(title="Select Node.js Installation Directory")
            if not selected_dir:
                if messagebox.askyesno("Cancel Installation", "No directory selected. Do you want to cancel the installation?"):
                    sys.exit(1)
                else:
                    continue
            node_exe = os.path.join(selected_dir, "node.exe")
            if os.path.exists(node_exe):
                print(f"Using Node.js at {node_exe}")
                break
            else:
                messagebox.showerror("Invalid Directory", "The selected directory does not contain node.exe. Please select a valid Node.js installation directory.")

def install_git():
    git_path = check_default_git()
    if git_path:
        print(f"Found Git at {git_path}")
    else:
        messagebox.showerror("Git Not Found", "Git is not installed in the default locations. Please install Git manually from https://git-scm.com/downloads/")
        sys.exit(1)

def main():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Installation", "Please select the installation directory.")
    base_path = filedialog.askdirectory(title="Select Installation Directory")
    if not base_path:
        messagebox.showerror("Error", "No directory selected. Installation cancelled.")
        sys.exit(1)

    # Check for required commands
    if not check_command_exists("python") and not check_command_exists("python3"):
        install_python()
    if not check_command_exists("node"):
        install_node()
        if not check_command_exists("node"):
            messagebox.showerror("Error", "Node.js is still not installed. Installation cannot continue.")
            sys.exit(1)
    if not check_command_exists("git"):
        install_git()

    venv_path = os.path.join(base_path, "venv")
    create_virtualenv(venv_path)

    if platform.system() == "Windows":
        venv_python = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(venv_path, "bin", "python")

    install_python_dependencies(venv_python)
    if check_command_exists("node"):
        install_frontend_dependencies(base_path)

    backend_process = start_backend_server(venv_python, base_path)
    time.sleep(5)  # Wait for backend to start

    frontend_process = start_frontend_server(base_path)
    time.sleep(5)  # Wait for frontend to start

    open_browser()
    create_desktop_shortcut(base_path)

    print("\nInstallation and setup complete.")
    print("To start the program later, activate the virtual environment and run:")
    if platform.system() == "Windows":
        print(r"venv\\Scripts\\activate")
    else:
        print("source venv/bin/activate")
    print("Then start backend with:")
    print(f"{venv_python} -m uvicorn backend.api:app --host 0.0.0.0 --port 8000")
    print("And start frontend with:")
    print("cd frontend && npm start")

    print("\nPress Ctrl+C to stop the servers and exit.")
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("Stopping servers...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main()
