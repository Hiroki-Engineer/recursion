import typer

from commands.reverse import app as reverse_app
from logging_config import setup_logging

app = typer.Typer()

app.add_typer(reverse_app)

if __name__ == "__main__":
    setup_logging()
    app()
