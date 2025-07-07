import os
import sys
import getpass
import platform
import json
from pathlib import Path
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def save_key(key, key_path):
    with open(key_path, 'wb') as f:
        f.write(key)

def load_key(key_path):
    with open(key_path, 'rb') as f:
        return f.read()

def encrypt_token(token, key):
    f = Fernet(key)
    return f.encrypt(token.encode())

def decrypt_token(token_encrypted, key):
    f = Fernet(key)
    return f.decrypt(token_encrypted).decode()

def get_config_dir():
    home = Path.home()
    config_dir = home / '.project_management'
    config_dir.mkdir(exist_ok=True)
    return config_dir

def save_token_encrypted(token_encrypted, config_dir):
    token_path = config_dir / 'github_token.enc'
    with open(token_path, 'wb') as f:
        f.write(token_encrypted)

def load_token_encrypted(config_dir):
    token_path = config_dir / 'github_token.enc'
    if token_path.exists():
        with open(token_path, 'rb') as f:
            return f.read()
    return None

def save_key_file(key, config_dir):
    key_path = config_dir / 'key.key'
    with open(key_path, 'wb') as f:
        f.write(key)

def load_key_file(config_dir):
    key_path = config_dir / 'key.key'
    if key_path.exists():
        with open(key_path, 'rb') as f:
            return f.read()
    return None

def prompt_github_token():
    print("This project management package requires a GitHub token for private repository access.")
    print("Please generate a personal access token with appropriate scopes from https://github.com/settings/tokens")
    token = getpass.getpass("Enter your GitHub token (input hidden): ")
    return token.strip()

def main():
    config_dir = get_config_dir()
    key = load_key_file(config_dir)
    if not key:
        key = generate_key()
        save_key_file(key, config_dir)

    token_encrypted = load_token_encrypted(config_dir)
    if token_encrypted:
        try:
            token = decrypt_token(token_encrypted, key)
            print("GitHub token loaded successfully from secure storage.")
            return
        except Exception:
            print("Failed to decrypt stored GitHub token. Re-enter token.")

    token = prompt_github_token()
    token_encrypted = encrypt_token(token, key)
    save_token_encrypted(token_encrypted, config_dir)
    print(f"GitHub token saved securely in {config_dir}")

if __name__ == "__main__":
    main()
