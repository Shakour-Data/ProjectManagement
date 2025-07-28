import os
import subprocess
import sys
import unittest
import tempfile
import shutil
from unittest.mock import patch, MagicMock

class TestInstallationSetup(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory to simulate installation directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove temporary directory after test
        shutil.rmtree(self.test_dir)

    def test_virtualenv_creation(self):
        venv_path = os.path.join(self.test_dir, "venv")
        # Run the virtualenv creation command
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        self.assertTrue(os.path.exists(venv_path))
        self.assertTrue(os.path.isdir(venv_path))

    def test_python_dependencies_installation(self):
        venv_path = os.path.join(self.test_dir, "venv")
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        if os.name == "nt":
            venv_python = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            venv_python = os.path.join(venv_path, "bin", "python")
        # Upgrade pip and install requirements
        subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])

    @patch('subprocess.run')
    def test_frontend_dependencies_installation(self, mock_run):
        frontend_path = os.path.join(os.getcwd(), "frontend")
        self.assertTrue(os.path.exists(frontend_path))
        mock_run.return_value = MagicMock(returncode=0)
        result = subprocess.run("npm install", shell=True, cwd=frontend_path)
        self.assertEqual(result.returncode, 0)

    @patch('subprocess.Popen')
    def test_backend_server_start(self, mock_popen):
        venv_path = os.path.join(self.test_dir, "venv")
        # Mock subprocess.check_call to avoid actual venv creation
        with patch('subprocess.check_call') as mock_check_call:
            mock_check_call.return_value = None
            subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        if os.name == "nt":
            venv_python = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            venv_python = os.path.join(venv_path, "bin", "python")
        mock_proc = MagicMock()
        mock_proc.terminate.return_value = None
        mock_proc.wait.return_value = 0
        mock_popen.return_value = mock_proc
        backend_cmd = [venv_python, "-m", "uvicorn", "backend.api:app", "--host", "127.0.0.1", "--port", "8000"]
        proc = subprocess.Popen(backend_cmd, cwd=os.getcwd())
        proc.terminate()
        proc.wait()
        self.assertEqual(proc.wait(), 0)

    @patch('subprocess.Popen')
    def test_frontend_server_start(self, mock_popen):
        frontend_path = os.path.join(os.getcwd(), "frontend")
        mock_proc = MagicMock()
        mock_proc.terminate.return_value = None
        mock_proc.wait.return_value = 0
        mock_popen.return_value = mock_proc
        proc = subprocess.Popen(["npm", "start"], cwd=frontend_path, shell=True)
        proc.terminate()
        proc.wait()
        self.assertEqual(proc.wait(), 0)

if __name__ == "__main__":
    unittest.main()
