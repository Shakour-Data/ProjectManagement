import argparse
import argparse
from Project_Management import main as main_module

def main_cli():
    parser = argparse.ArgumentParser(description='Project Management Tool CLI')
    parser.add_argument('command', choices=['install', 'start', 'status'], help='Command to run')
    args = parser.parse_args()

    if args.command == 'install':
        main_module.install()
    elif args.command == 'start':
        main_module.start()
    elif args.command == 'status':
        main_module.status()

def main():
    main_cli()

if __name__ == '__main__':
    main()
