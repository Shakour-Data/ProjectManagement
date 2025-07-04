import argparse

def main():
    parser = argparse.ArgumentParser(description="Project Management Tool CLI")
    # Removed explicit --help argument to avoid conflict with default help
    parser.add_argument('command', nargs='?', help='Command to run: setup, status, etc.')

    args = parser.parse_args()

    if args.command == 'setup':
        print("Setup completed successfully.")
    elif args.command == 'status':
        print("Configuration: ...")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
