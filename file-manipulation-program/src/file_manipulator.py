import typer

from commands.copy import app as copy_app
from commands.duplicate_contents import app as duplicate_contents_app
from commands.replace_string import app as replace_string_app
from commands.reverse import app as reverse_app
from logging_config import setup_logging

app = typer.Typer()

app.add_typer(reverse_app)
app.add_typer(copy_app)
app.add_typer(duplicate_contents_app)
app.add_typer(replace_string_app)

if __name__ == "__main__":
    setup_logging()
    app()
