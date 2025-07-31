# Config and Token Management Module

## Overview
The `config_and_token_management` module provides functions to securely manage configuration data and encrypted tokens. It uses symmetric encryption (Fernet) to encrypt and decrypt tokens, and JSON files to store configuration data.

## Functions

- `generate_key()`
  - Generates a new encryption key and saves it to a file.
  - Returns: The generated key.

- `load_key()`
  - Loads the encryption key from file or generates a new one if not found.
  - Returns: The encryption key.

- `encrypt_token(token)`
  - Encrypts a token string and saves it to a file.
  - Parameters:
    - `token` (str): The token to encrypt.

- `decrypt_token()`
  - Decrypts and returns the token string from the encrypted file.
  - Returns: The decrypted token string or `None` if no token file exists.

- `save_config(config_data)`
  - Saves configuration data as JSON to a config file.
  - Parameters:
    - `config_data` (dict): Configuration data to save.

- `load_config()`
  - Loads configuration data from the config file.
  - Returns: Configuration data dictionary or empty dict if file not found.

## Usage
Example usage to save config and encrypt a token:

```python
if __name__ == '__main__':
    config = {
        "github_repo": "user/repo",
        "user_name": "username"
    }
    save_config(config)
    token = "your_github_token_here"
    encrypt_token(token)
    print("Config and token saved securely.")
```

---

This documentation provides an overview of the `config_and_token_management` module to assist developers in securely managing configuration and token data.
