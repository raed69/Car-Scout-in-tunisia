import sys


if __name__ == "__main__":
    # "python main.py" opens the chat page; "python main.py cli" keeps the chat in the terminal.
    if sys.argv[1:] == ["cli"]:
        from backend.app.cli import run_cli

        run_cli()
    else:
        from backend.app.api import run_web

        run_web()
