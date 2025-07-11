import argparse
from project_management import main as main_module

def main_cli():
    parser = argparse.ArgumentParser(description='Project Management Tool CLI')
    parser.add_argument('command', choices=['install', 'start', 'status', 'setup', 'help'], help='Command to run')
    args = parser.parse_args()

    if args.command == 'install':
        main_module.install()
    elif args.command == 'start':
        main_module.start()
    elif args.command == 'status':
        main_module.status()
    elif args.command == 'setup':
        main_module.setup()
    elif args.command == 'help':
        main_module.help()

def main():
    main_cli()

if __name__ == '__main__':
    main()
