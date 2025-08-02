import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestSetupPostInstallServiceFunctions(unittest.TestCase):
    """Test cases for setup_post_install service functions according to Unit_Testing.md standards."""

    def setUp(self):
        """Setup any necessary test data or state."""
        pass

    # Service Function Tests - Test individual backend service functions for correct output
    @patch('project_management.setup_post_install.Path.home')
    @patch('project_management.setup_post_install.Path.mkdir')
    def test_get_config_dir_success(self, mock_mkdir, mock_home):
        """Test get_config_dir with successful execution."""
        # Setup mocks
        mock_home.return_value = "/home/user"
        mock_mkdir.return_value = None
        
        # Import the module
        from project_management.setup_post_install import get_config_dir
        
        config_dir = get_config_dir()
        
        # Verify results
        self.assertEqual(str(config_dir), "/home/user/.project_management")
        mock_mkdir.assert_called_once_with(exist_ok=True)

    @patch('project_management.setup_post_install.Fernet')
    def test_encrypt_token_success(self, mock_fernet):
        """Test encrypt_token with successful execution."""
        # Setup mock
        mock_fernet_instance = MagicMock()
        mock_fernet_instance.encrypt.return_value = b"encrypted_token"
        mock_fernet.return_value = mock_fernet_instance
        
        # Import the module
        from project_management.setup_post_install import encrypt_token
        
        encrypted = encrypt_token("token123", b"key")
        
        # Verify results
        self.assertEqual(encrypted, b"encrypted_token")
        mock_fernet_instance.encrypt.assert_called_once_with("token123".encode())

    @patch('project_management.setup_post_install.Fernet')
    def test_decrypt_token_success(self, mock_fernet):
        """Test decrypt_token with successful execution."""
        # Setup mock
        mock_fernet_instance = MagicMock()
        mock_fernet_instance.decrypt.return_value = b"token123"
        mock_fernet.return_value = mock_fernet_instance
        
        # Import the module
        from project_management.setup_post_install import decrypt_token
        
        decrypted = decrypt_token(b"encrypted_token", b"key")
        
        # Verify results
        self.assertEqual(decrypted, "token123")
        mock_fernet_instance.decrypt.assert_called_once_with(b"encrypted_token")

    @patch('project_management.setup_post_install.os.path.exists')
    @patch('project_management.setup_post_install.open')
    def test_load_key_file_exists(self, mock_open, mock_exists):
        """Test load_key_file when key file exists."""
        # Setup mocks
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.read.return_value = b"key_data"
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Import the module
        from project_management.setup_post_install import load_key_file
        
        key = load_key_file("/config/dir")
        
        # Verify results
        self.assertEqual(key, b"key_data")
        mock_open.assert_called_once_with("/config/dir/key.key", 'rb')

    @patch('project_management.setup_post_install.os.path.exists')
    def test_load_key_file_not_exists(self, mock_exists):
        """Test load_key_file when key file does not exist."""
        # Setup mock
        mock_exists.return_value = False
        
        # Import the module
        from project_management.setup_post_install import load_key_file
        
        key = load_key_file("/config/dir")
        
        # Verify results
        self.assertIsNone(key)

    @patch('project_management.setup_post_install.os.path.exists')
    @patch('project_management.setup_post_install.open')
    def test_load_token_encrypted_exists(self, mock_open, mock_exists):
        """Test load_token_encrypted when token file exists."""
        # Setup mocks
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.read.return_value = b"token_data"
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Import the module
        from project_management.setup_post_install import load_token_encrypted
        
        token = load_token_encrypted("/config/dir")
        
        # Verify results
        self.assertEqual(token, b"token_data")
        mock_open.assert_called_once_with("/config/dir/github_token.enc", 'rb')

    @patch('project_management.setup_post_install.os.path.exists')
    def test_load_token_encrypted_not_exists(self, mock_exists):
        """Test load_token_encrypted when token file does not exist."""
        # Setup mock
        mock_exists.return_value = False
        
        # Import the module
        from project_management.setup_post_install import load_token_encrypted
        
        token = load_token_encrypted("/config/dir")
        
        # Verify results
        self.assertIsNone(token)

    @patch('project_management.setup_post_install.getpass.getpass')
    def test_prompt_github_token_success(self, mock_getpass):
        """Test prompt_github_token with successful execution."""
        # Setup mock
        mock_getpass.return_value = "token123"
        
        # Import the module
        from project_management.setup_post_install import prompt_github_token
        
        token = prompt_github_token()
        
        # Verify results
        self.assertEqual(token, "token123")
        mock_getpass.assert_called_once_with("Enter your GitHub token (input hidden): ")

if __name__ == "__main__":
    unittest.main()
