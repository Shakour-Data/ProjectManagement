import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import subprocess
import sys

# Add the project root to the path so we can import the module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestSetupInitialization(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        pass

    # Test 1: Test create_virtualenv when directory does not exist
    @patch("os.path.exists", return_value=False)
    @patch("project_management.modules.main_modules.setup_initialization.venv.create")
    @patch("builtins.print")
    def test_create_virtualenv_directory_not_exists(self, mock_print, mock_venv_create, mock_exists):
        from project_management.modules.main_modules.setup_initialization import create_virtualenv
        create_virtualenv('test_env')
        mock_venv_create.assert_called_once_with('test_env', with_pip=True)
        mock_print.assert_any_call("Creating virtual environment at test_env...")

    # Test 2: Test create_virtualenv when directory already exists
    @patch("os.path.exists", return_value=True)
    @patch("builtins.print")
    def test_create_virtualenv_directory_exists(self, mock_print, mock_exists):
        from project_management.modules.main_modules.setup_initialization import create_virtualenv
        create_virtualenv('test_env')
        mock_print.assert_called_once_with("Virtual environment already exists at test_env.")

    # Test 3: Test install_dependencies when pip executable exists and requirements file exists
    @patch("os.path.exists", side_effect=lambda path: path.endswith('bin/pip') or path.endswith('requirements.txt'))
    @patch("subprocess.check_call")
    @patch("builtins.print")
    def test_install_dependencies_pip_and_requirements_exist(self, mock_print, mock_subprocess, mock_exists):
        from project_management.modules.main_modules.setup_initialization import install_dependencies
        install_dependencies('test_env', 'requirements.txt')
        mock_subprocess.assert_called_once_with(['test_env/bin/pip', 'install', '-r', 'requirements.txt'])
        mock_print.assert_any_call("Installing dependencies from requirements.txt...")

    # Test 4: Test install_dependencies when pip executable does not exist
    @patch("os.path.exists", side_effect=lambda path: path.endswith('requirements.txt'))
    @patch("builtins.print")
    def test_install_dependencies_pip_not_exists(self, mock_print, mock_exists):
        from project_management.modules.main_modules.setup_initialization import install_dependencies
        install_dependencies('test_env', 'requirements.txt')
        mock_print.assert_called_once_with("pip not found in virtual environment. Please check the environment setup.")

    # Test 5: Test install_dependencies when requirements file does not exist
    @patch("os.path.exists", side_effect=lambda path: path.endswith('bin/pip'))
    @patch("builtins.print")
    def test_install_dependencies_requirements_not_exists(self, mock_print, mock_exists):
        from project_management.modules.main_modules.setup_initialization import install_dependencies
        install_dependencies('test_env', 'requirements.txt')
        mock_print.assert_called_once_with("requirements.txt not found. Skipping dependency installation.")

    # Test 6: Test initialize_git_repo when .git directory does not exist
    @patch("os.path.exists", return_value=False)
    @patch("subprocess.run")
    @patch("builtins.print")
    def test_initialize_git_repo_not_exists(self, mock_print, mock_subprocess, mock_exists):
        from project_management.modules.main_modules.setup_initialization import initialize_git_repo
        initialize_git_repo()
        mock_subprocess.assert_called_once_with(['git', 'init'], check=True)
        mock_print.assert_any_call("Initializing git repository...")

    # Test 7: Test initialize_git_repo when .git directory already exists
    @patch("os.path.exists", return_value=True)
    @patch("builtins.print")
    def test_initialize_git_repo_exists(self, mock_print, mock_exists):
        from project_management.modules.main_modules.setup_initialization import initialize_git_repo
        initialize_git_repo()
        mock_print.assert_called_once_with("Git repository already initialized.")

    # Test 8: Test ensure_gitignore_excludes_venv when .gitignore does not exist
    @patch("os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_ensure_gitignore_excludes_venv_no_gitignore(self, mock_print, mock_open_file, mock_exists):
        from project_management.modules.main_modules.setup_initialization import ensure_gitignore_excludes_venv
        ensure_gitignore_excludes_venv('.gitignore')
        mock_open_file.assert_called_once_with('.gitignore', 'w')
        mock_print.assert_called_once_with("Updated .gitignore to exclude virtual environment directories.")

    # Test 9: Test ensure_gitignore_excludes_venv when .gitignore exists and needs update
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="existing_content")
    @patch("builtins.print")
    def test_ensure_gitignore_excludes_venv_exists_needs_update(self, mock_print, mock_open_file, mock_exists):
        from project_management.modules.main_modules.setup_initialization import ensure_gitignore_excludes_venv
        ensure_gitignore_excludes_venv('.gitignore')
        mock_open_file.assert_called_with('.gitignore', 'w')
        mock_print.assert_called_once_with("Updated .gitignore to exclude virtual environment directories.")

    # Test 10: Test ensure_gitignore_excludes_venv when .gitignore exists and already has venv dirs
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="venv/\n.venv/\nENV/\nenv/")
    @patch("builtins.print")
    def test_ensure_gitignore_excludes_venv_exists_already_updated(self, mock_print, mock_open_file, mock_exists):
        from project_management.modules.main_modules.setup_initialization import ensure_gitignore_excludes_venv
        ensure_gitignore_excludes_venv('.gitignore')
        mock_print.assert_called_once_with(".gitignore already excludes virtual environment directories.")

    # Test 11: Test create_requirements_file when file does not exist
    @patch("os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_create_requirements_file_not_exists(self, mock_print, mock_open_file, mock_exists):
        from project_management.modules.main_modules.setup_initialization import create_requirements_file
        create_requirements_file('requirements.txt')
        mock_open_file.assert_called_once_with('requirements.txt', 'w')
        mock_print.assert_called_once_with("Created requirements.txt. Please add your project dependencies to this file.")

    # Test 12: Test create_requirements_file when file already exists
    @patch("os.path.exists", return_value=True)
    @patch("builtins.print")
    def test_create_requirements_file_exists(self, mock_print, mock_exists):
        from project_management.modules.main_modules.setup_initialization import create_requirements_file
        create_requirements_file('requirements.txt')
        mock_print.assert_called_once_with("requirements.txt already exists.")

    # Test 13: Test main function execution
    @patch("project_management.modules.main_modules.setup_initialization.ensure_gitignore_excludes_venv")
    @patch("project_management.modules.main_modules.setup_initialization.initialize_git_repo")
    @patch("project_management.modules.main_modules.setup_initialization.create_requirements_file")
    @patch("project_management.modules.main_modules.setup_initialization.create_virtualenv")
    @patch("project_management.modules.main_modules.setup_initialization.install_dependencies")
    def test_main_function(self, mock_install, mock_create_venv, mock_create_req, mock_init_git, mock_ensure_gitignore):
        from project_management.modules.main_modules.setup_initialization import main
        main()
        mock_ensure_gitignore.assert_called_once()
        mock_init_git.assert_called_once()
        mock_create_req.assert_called_once()
        mock_create_venv.assert_called_once()
        mock_install.assert_called_once()

    # Test 14: Test create_virtualenv with custom directory
    @patch("os.path.exists", return_value=False)
    @patch("project_management.modules.main_modules.setup_initialization.venv.create")
    @patch("builtins.print")
    def test_create_virtualenv_custom_directory(self, mock_print, mock_venv_create, mock_exists):
        from project_management.modules.main_modules.setup_initialization import create_virtualenv
        create_virtualenv('custom_env')
        mock_venv_create.assert_called_once_with('custom_env', with_pip=True)
        mock_print.assert_any_call("Creating virtual environment at custom_env...")

    # Test 15: Test install_dependencies with custom paths
    @patch("os.path.exists", side_effect=lambda path: path.endswith('bin/pip') or path.endswith('custom_requirements.txt'))
    @patch("subprocess.check_call")
    @patch("builtins.print")
    def test_install_dependencies_custom_paths(self, mock_print, mock_subprocess, mock_exists):
        from project_management.modules.main_modules.setup_initialization import install_dependencies
        install_dependencies('custom_env', 'custom_requirements.txt')
        mock_subprocess.assert_called_once_with(['custom_env/bin/pip', 'install', '-r', 'custom_requirements.txt'])
        mock_print.assert_any_call("Installing dependencies from custom_requirements.txt...")

    # Test 16: Test ensure_gitignore_excludes_venv with custom venv directories
    @patch("os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_ensure_gitignore_excludes_venv_custom_venv_dirs(self, mock_print, mock_open_file, mock_exists):
        from project_management.modules.main_modules.setup_initialization import ensure_gitignore_excludes_venv
        custom_venv_dirs = ['custom_venv/', 'my_env/']
        ensure_gitignore_excludes_venv('.gitignore', custom_venv_dirs)
        mock_open_file.assert_called_once_with('.gitignore', 'w')
        mock_print.assert_called_once_with("Updated .gitignore to exclude virtual environment directories.")

    # Test 17: Test create_requirements_file with custom filename
    @patch("os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_create_requirements_file_custom_filename(self, mock_print, mock_open_file, mock_exists):
        from project_management.modules.main_modules.setup_initialization import create_requirements_file
        create_requirements_file('custom_requirements.txt')
        mock_open_file.assert_called_once_with('custom_requirements.txt', 'w')
        mock_print.assert_called_once_with("Created custom_requirements.txt. Please add your project dependencies to this file.")

    # Test 18: Test initialize_git_repo with subprocess error
    @patch("os.path.exists", return_value=False)
    @patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, 'git init'))
    @patch("builtins.print")
    def test_initialize_git_repo_subprocess_error(self, mock_print, mock_subprocess, mock_exists):
        from project_management.modules.main_modules.setup_initialization import initialize_git_repo
        with self.assertRaises(subprocess.CalledProcessError):
            initialize_git_repo()

    # Test 19: Test install_dependencies with subprocess error
    @patch("os.path.exists", side_effect=lambda path: path.endswith('bin/pip') or path.endswith('requirements.txt'))
    @patch("subprocess.check_call", side_effect=subprocess.CalledProcessError(1, 'pip install'))
    @patch("builtins.print")
    def test_install_dependencies_subprocess_error(self, mock_print, mock_subprocess, mock_exists):
        from project_management.modules.main_modules.setup_initialization import install_dependencies
        with self.assertRaises(subprocess.CalledProcessError):
            install_dependencies('test_env', 'requirements.txt')

    # Test 20: Test ensure_gitignore_excludes_venv with unicode content
    @patch("os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_ensure_gitignore_excludes_venv_unicode_content(self, mock_print, mock_open_file, mock_exists):
        from project_management.modules.main_modules.setup_initialization import ensure_gitignore_excludes_venv
        unicode_venv_dirs = ['虚拟环境/', '环境/']  # "virtual_env/" and "env/" in Chinese
        ensure_gitignore_excludes_venv('.gitignore', unicode_venv_dirs)
        mock_open_file.assert_called_once_with('.gitignore', 'w')
        mock_print.assert_called_once_with("Updated .gitignore to exclude virtual environment directories.")

if __name__ == "__main__":
    unittest.main()
