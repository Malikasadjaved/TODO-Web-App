"""Entry point for Todo Application."""

from src.todo.cli import run_cli


def main():
    """Main entry point."""
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Goodbye!\n")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}\n")
        raise


if __name__ == "__main__":
    main()
