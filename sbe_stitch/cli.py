from pathlib import Path
from typer import Typer
from typing import Optional, Tuple
from sbe_stitch.stitch import stitch as _stitch

app = Typer()


@app.command()
def hello(name: str) -> None:
    print(f"Hello {name or ''}")


@app.command()
def stitch(output_path: str, input_directory: str, preferred_dimensions: Optional[Tuple[int, int]] = None) -> None:
    _stitch(Path(output_path), Path(input_directory), preferred_dimensions)
