import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestSetupPostInstallDataValidation(unittest.TestCase):
    """Test cases for setup_post_install data validation according to Unit_Testing.md standards."""

    def setUp(self):
        """Setup any necessary test data or state."""
        pass

    # Data Validation Tests - Verify data validation logic in models and services
    @patch('project_management.setup_post_install.Path.home')
    @patch('project_management.setup_post_install.Path.mkdir')
    def test_get_config_dir_with_special_characters(self, mock_mkdir, mock_home):
        """Test get_config_dir with home directory containing special characters."""
        # Setup mocks with special characters
        mock_home.return_value = "/home/user#123"
        mock_mkdir.return_value = None
        
        # Import the module
        from project_management.setup_post_install import get_config_dir
        
        config_dir = get_config_dir()
        
        # Verify results
        self.assertEqual(str(config_dir), "/home/user#123/.project_management")

    @patch('project_management.setup_post_install.Path.home')
    @patch('project_management.setup_post_install.Path.mkdir')
    def test_get_config_dir_with_unicode(self, mock_mkdir, mock_home):
        """Test get_config_dir with home directory containing unicode characters."""
        # Setup mocks with unicode characters
        mock_home.return_value = "/home/کاربر"
        mock_mkdir.return_value = None
        
        # Import the module
        from project_management.setup_post_install import get_config_dir
        
        config_dir = get_config_dir()
        
        # Verify results
        self.assertEqual(str(config_dir), "/home/کاربر/.project_management")

    @patch('project_management.setup_post_install.Path.home')
    @patch('project_management.setup_post_install.Path.mkdir')
    def test_get_config_dir_with_long_path(self, mock_mkdir, mock_home):
        """Test get_config_dir with long home directory path."""
        # Setup mocks with long path
        long_path = "/home/user" + "a" * 1000
        mock_home.return_value = long_path
        mock_mkdir.return_value = None
        
        # Import the module
        from project_management.setup_post_install import get_config_dir
        
        config_dir = get_config_dir()
        
        # Verify results
        self.assertEqual(str(config_dir), long_path + "/.project_management")

    @patch('project_management.setup_post_install.Fernet')
    def test_encrypt_token_with_special_characters(self, mock_fernet):
        """Test encrypt_token with token containing special characters."""
        # Setup mock
        mock_fernet_instance = MagicMock()
        mock_fernet_instance.encrypt.return_value = b"encrypted_token"
        mock_fernet.return_value = mock_fernet_instance
        
        # Import the module
        from project_management.setup_post_install import encrypt_token
        
        # Test with token containing special characters
        encrypted = encrypt_token("token#123!@#", b"key")
        
        # Verify results
        self.assertEqual(encrypted, b"encrypted_token")
        mock_fernet_instance.encrypt.assert_called_once_with("token#123!@#".encode())

    @patch('project_management.setup_post_install.Fernet')
    def test_encrypt_token_with_unicode(self, mock_fernet):
        """Test encrypt_token with token containing unicode characters."""
        # Setup mock
        mock_fernet_instance = MagicMock()
        mock_fernet_instance.encrypt.return_value = b"encrypted_token"
        mock_fernet.return_value = mock_fernet_instance
        
        # Import the module
        from project_management.setup_post_install import encrypt_token
        
        # Test with token containing unicode characters
        encrypted = encrypt_token("توکن123", b"key")
        
        # Verify results
        self.assertEqual(encrypted, b"encrypted_token")
        mock_fernet_instance.encrypt.assert_called_once_with("توکن123".encode())

    @patch('project_management.setup_post_install.Fernet')
    def test_encrypt_token_with_long_token(self, mock_fernet):
        """Test encrypt_token with long token."""
        # Setup mock
        mock_fernet_instance = MagicMock()
        mock_fernet_instance.encrypt.return_value = b"encrypted_token"
        mock_fernet.return_value = mock_fernet_instance
        
        # Import the module
        from project_management.setup_post_install import encrypt_token
        
        # Test with long token
        long_token = "a" * 1000
        encrypted = encrypt_token(long_token, b"key")
        
        # Verify results
        self.assertEqual(encrypted, b"encrypted_token")
        mock_fernet_instance.encrypt.assert_called_once_with(long_token.encode())

    @patch('project_management.setup_post_install.Fernet')
    def test_decrypt_token_with_special_characters(self, mock_fernet):
        """Test decrypt_token with encrypted token containing special characters."""
        # Setup mock
        mock_fernet_instance = MagicMock()
        mock_fernet_instance.decrypt.return_value = "token#123!@#".encode()
        mock_fernet.return_value = mock_fernet_instance
        
        # Import the module
        from project_management.setup_post_install import decrypt_token
        
        decrypted = decrypt_token(b"encrypted_token", b"key")
        
        # Verify results
        self.assertEqual(decrypted, "token#123!@#")
        mock_fernet_instance.decrypt.assert_called_once_with(b"encrypted_token")

    @patch('project_management.setup_post_install.Fernet')
    def test_decrypt_token_with_unicode(self, mock_fernet):
        """Test decrypt_token with encrypted token containing unicode characters."""
        # Setup mock
        mock_fernet_instance = MagicMock()
        mock_fernet_instance.decrypt.return_value = "توکن123".encode()
        mock_fernet.return_value = mock_fernet_instance
        
        # Import the module
        from project_management.setup_post_install import decrypt_token
        
        decrypted = decrypt_token(b"encrypted_token", b"key")
        
        # Verify results
        self.assertEqual(decrypted, "توکن123")
        mock_fernet_instance.decrypt.assert_called_once_with(b"encrypted_token")

    @patch('project_management.setup_post_install.Fernet.generate_key')
    @patch('project_management.setup_post_install.getpass.getpass')
    def test_prompt_github_token_with_special_characters(self, mock_getpass, mock_generate_key):
        """Test prompt_github_token with token containing special characters."""
        # Setup mock
        mock_getpass.return_value = "token#123!@#"
        
        # Import the module
        from project_management.setup_post_install import prompt_github_token
        
        token = prompt_github_token()
        
        # Verify results
        self.assertEqual(token, "token#123!@#")
        mock_getpass.assert_called_once_with("Enter your GitHub token (input hidden): ")

    @patch('project_management.setup_post_install.getpass.getpass')
    def test_prompt_github_token_with_unicode(self, mock_getpass):
        """Test prompt_github_token with token containing unicode characters."""
        # Setup mock
        mock_getpass.return_value = "توکن123"
        
        # Import the module
        from project_management.setup_post_install import prompt_github_token
        
        token = prompt_github_token()
        
        # Verify results
        self.assertEqual(token, "توکن123")
        mock_getpass.assert_called_once_with("Enter your GitHub token (input hidden): ")

    @patch('project_management.setup_post_install.getpass.getpass')
    def test_prompt_github_token_with_long_token(self, mock_getpass):
        """Test prompt_github_token with long token."""
        # Setup mock
        long_token = "a" * 1000
        mock_getpass.return_value = long_token
        
        # Import the module
        from project_management.setup_post_install import prompt_github_token
        
        token = prompt_github_token()
        
        # Verify results
        self.assertEqual(token, long_token)
        mock_getpass.assert_called_once_with("Enter your GitHub token (input hidden): ")

    @patch('project_management.setup_post_install.getpass.getpass')
    def test_prompt_github_token_with_whitespace(self, mock_getpass):
        """Test prompt_github_token with token containing whitespace."""
        # Setup mock
        mock_getpass.return_value = "  token123  "
        
        # Import the module
        from project_management.setup_post_install import prompt_github_token
        
        token = prompt_github_token()
        
        # Verify results
        self.assertEqual(token, "  token123  ")
        mock_getpass.assert_called_once_with("Enter your GitHub token (input hidden): ")

    @patch('project_management.setup_post_install.getpass.getpass')
    def test_prompt_github_token_empty_input(self, mock_getpass):
        """Test prompt_github_token with empty input."""
        # Setup mock
        mock_getpass.return_value = ""
        
        # Import the module
        from project_management.setup_post_install import prompt_github_token
        
        token = prompt_github_token()
        
        # Verify results
        self.assertEqual(token, "")
        mock_getpass.assert_called_once_with("Enter your GitHub token (input hidden): ")

    @patch('project_management.setup_post_install.os.path.exists')
    @patch('project_management.setup_post_install.open')
    def test_load_key_file_with_special_characters(self, mock_open, mock_exists):
        """Test load_key_file with config directory containing special characters."""
        # Setup mocks
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.read.return_value = b"key_data"
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Import the module
        from project_management.setup_post_install import load_key_file
        
        key = load_key_file("/config/dir#123")
        
        # Verify results
        self.assertEqual(key, b"key_data")
        mock_open.assert_called_once_with("/config/dir#123/key.key", 'rb')

    @patch('project_management.setup_post_install.os.path.exists')
    @patch('project_management.setup_post_install.open')
    def test_load_token_encrypted_with_special_characters(self, mock_open, mock_exists):
        """Test load_token_encrypted with config directory containing special characters."""
        # Setup mocks
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.read.return_value = b"token_data"
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Import the module
        from project_management.setup_post_install import load_token_encrypted
        
        token = load_token_encrypted("/config/dir#123")
        
        # Verify results
        self.assertEqual(token, b"token_data")
        mock_open.assert_called_once_with("/config/dir#123/github_token.enc", 'rb')

if __name__ == "__main__":
    unittest.main()
