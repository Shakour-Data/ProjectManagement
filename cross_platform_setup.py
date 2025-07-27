import os
import sys
import subprocess
import platform
import shutil
import time

def run_command(command, shell=False):
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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

def install_frontend_dependencies():
    print("Installing frontend dependencies...")
    if not os.path.exists("frontend"):
        print("Frontend directory not found!")
        sys.exit(1)
    run_command(["npm", "install"], shell=True, cwd="frontend")

def start_backend_server(venv_python):
    print("Starting backend server...")
    # Use subprocess.Popen to run in background
    backend_cmd = [venv_python, "-m", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
    backend_process = subprocess.Popen(backend_cmd)
    return backend_process

def start_frontend_server():
    print("Starting frontend server...")
    frontend_process = subprocess.Popen(["npm", "start"], cwd="frontend", shell=True)
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

def create_desktop_shortcut():
    system = platform.system()
    home = os.path.expanduser("~")
    desktop = ""
    shortcut_name = "ProjectManagement"

    if system == "Windows":
        desktop = os.path.join(home, "Desktop")
        shortcut_path = os.path.join(desktop, f"{shortcut_name}.lnk")
        try:
            import pythoncom
            from win32com.shell import shell, shellcon
            from win32com.client import Dispatch

            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            # Target is python executable with this script
            python_exe = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")
            script_path = os.path.join(os.getcwd(), "cross_platform_setup.py")
            shortcut.Targetpath = python_exe
            shortcut.Arguments = f'"{script_path}"'
            shortcut.WorkingDirectory = os.getcwd()
            shortcut.IconLocation = python_exe
            shortcut.save()
            print(f"Desktop shortcut created at {shortcut_path}")
        except ImportError:
            print("pywin32 is required to create Windows shortcuts. Please install it manually.")
        except Exception as e:
            print(f"Failed to create Windows shortcut: {e}")

    elif system == "Darwin":
        desktop = os.path.join(home, "Desktop")
        shortcut_path = os.path.join(desktop, f"{shortcut_name}.command")
        try:
            with open(shortcut_path, "w") as f:
                f.write(f"#!/bin/bash\n")
                f.write(f"cd {os.getcwd()}\n")
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
                f.write(f"Exec=python3 {os.path.join(os.getcwd(), 'cross_platform_setup.py')}\n")
                f.write("Type=Application\n")
                f.write("Terminal=true\n")
                f.write(f"Icon=utilities-terminal\n")
                f.write("Categories=Utility;\n")
            os.chmod(shortcut_path, 0o755)
            print(f"Desktop shortcut created at {shortcut_path}")
        except Exception as e:
            print(f"Failed to create Linux shortcut: {e}")

def main():
    venv_path = os.path.join(os.getcwd(), "venv")
    create_virtualenv(venv_path)

    if platform.system() == "Windows":
        venv_python = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(venv_path, "bin", "python")

    install_python_dependencies(venv_python)
    install_frontend_dependencies()

    backend_process = start_backend_server(venv_python)
    time.sleep(5)  # Wait for backend to start

    frontend_process = start_frontend_server()
    time.sleep(5)  # Wait for frontend to start

    open_browser()
    create_desktop_shortcut()

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
