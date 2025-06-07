import logging
from pathlib import Path

import typer

from commands.utils import validate_file_exist

app = typer.Typer()

_logger = logging.getLogger()


@app.command()
def copy(inputpath: Path, outputpath: Path) -> None:
    _logger.info(f"inputpath: {inputpath.resolve()}\noutputpath: {outputpath.resolve()}\n")

    validate_file_exist(inputpath)

    with inputpath.open("r") as f:
        content = f.read()

    with outputpath.open("w") as f:
        f.write(content)
