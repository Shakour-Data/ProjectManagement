import argparse
import sys

def setup_cli():
    parser = argparse.ArgumentParser(description="Project Management Tool CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Example command: status
    parser_status = subparsers.add_parser('status', help='Show the current status of the project')
    parser_status.set_defaults(func=cmd_status)

    # Example command: generate-report
    parser_report = subparsers.add_parser('generate-report', help='Generate project reports')
    parser_report.add_argument('--type', choices=['progress', 'importance_urgency'], default='progress', help='Type of report to generate')
    parser_report.set_defaults(func=cmd_generate_report)

    # Add more commands here as needed

    # Added setup command
    parser_setup = subparsers.add_parser('setup', help='Run setup tasks')
    parser_setup.set_defaults(func=cmd_setup)

    return parser

def cmd_status(args):
    print("Project Management Tool CLI - Status")
    # Placeholder: Implement actual status logic here
    print("Configuration: All systems operational.")

def cmd_setup(args):
    print("Setup completed successfully.")
    # Placeholder: Implement actual setup logic here

def cmd_generate_report(args):
    if args.type == 'progress':
        from progress_report import generate_report
        generate_report()
        print("Progress report generated.")
    elif args.type == 'importance_urgency':
        from progress_report import generate_importance_urgency_report
        generate_importance_urgency_report()
        print("Importance and Urgency report generated.")
    else:
        print(f"Unknown report type: {args.type}")

def main():
    parser = setup_cli()
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
