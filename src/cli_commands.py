import argparse
import os
import json
from config_and_token_management import load_config, decrypt_token

def setup(args):
    print("Starting setup process...")
    # Here you would add setup logic, e.g., create virtualenv, install dependencies, etc.
    print("Setup completed successfully.")

def status(args):
    print("Fetching project management tool status...")
    config = load_config()
    token = decrypt_token()
    print("Configuration:")
    print(json.dumps(config, indent=4))
    if token:
        print("GitHub token is securely stored.")
    else:
        print("GitHub token not found.")
    # Additional status info can be added here

def main():
    parser = argparse.ArgumentParser(description="Project Management Tool CLI")
    subparsers = parser.add_subparsers()

    parser_setup = subparsers.add_parser('setup', help='Setup the project management tool')
    parser_setup.set_defaults(func=setup)

    parser_status = subparsers.add_parser('status', help='Show the current status of the tool')
    parser_status.set_defaults(func=status)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
