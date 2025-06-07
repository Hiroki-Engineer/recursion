import logging
from pathlib import Path

import typer

from commands.utils import validate_file_exist

app = typer.Typer()

_logger = logging.getLogger()


@app.command("replace-string")
def replace_string(inputpath: Path, old_string: str, new_string: str) -> None:
    _logger.info(f"inputpath: {inputpath.resolve()}\nold_string: {old_string}\nnew_string: {new_string}\n")

    validate_file_exist(inputpath)

    with inputpath.open("r") as f:
        content = f.read()

    with inputpath.open("w") as f:
        f.write(content.replace(old_string, new_string))
