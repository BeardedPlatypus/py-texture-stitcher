import json
from pathlib import Path
from rich import print
from rich.padding import Padding
from typing import Optional, Sequence, Tuple

from sbe_stitch import common
from sbe_stitch.description import StitchDescription
from sbe_stitch.description import SUFFIX as description_suffix


_PADDING = (0, 0, 0, 4)


def _retrieve_stitch_info_json(path: Path) -> Optional[StitchDescription]:
    if not path.exists():
        return None

    try:
        with path.open("r") as f:
            return StitchDescription.from_dict(json.load(f))
    except:  # noqa: E722
        return None


def _error_not_exists(path: Path) -> None:
    common.error(f"the provided path, '{path}', does not exist.")


def _info_description(path: Path, description: StitchDescription) -> None:
    common.info(f"'{path}'")

    lines = [
        Padding(f"Version: {description.metadata.version.to_str()}", _PADDING),
        Padding(f"Image Dimensions: {description.image_dimension.to_str()}", _PADDING),
        Padding(
            f"Stitch Dimensions: {description.stitch_dimension.to_str()}", _PADDING
        ),
        Padding(f"Images: {len(description.image_paths)}", _PADDING),
    ]

    for line in lines:
        print(line)
    for path in description.image_paths:
        print(Padding(str(path), (0, 0, 0, 8)))


def _warn_no_descriptions_directory(path: Path) -> None:
    common.warning(f"no descriptions found in '{path}'.")


def _warn_no_description_path(path: Path) -> None:
    common.warning(f"'{path}' is not a description.")


def _retrieve_stitch_infos_directory(
    path: Path,
) -> Sequence[Tuple[Path, StitchDescription]]:
    paths = path.glob(f"*{description_suffix}")
    descriptions = [(dp, d) for dp in paths if (d := _retrieve_stitch_info_json(dp))]

    if not descriptions:
        _warn_no_descriptions_directory(path)
    return descriptions


def _retrieve_stitch_infos_file(path: Path) -> Sequence[Tuple[Path, StitchDescription]]:
    description = _retrieve_stitch_info_json(path)

    if description:
        return [(path, description)]
    else:
        _warn_no_description_path(path)
        return []


def _retrieve_stitch_infos(path: Path) -> Sequence[Tuple[Path, StitchDescription]]:
    if path.is_dir():
        return _retrieve_stitch_infos_directory(path)

    if path.is_file():
        if path.suffix == ".png":
            path = path.with_suffix(description_suffix)

        if str(path).endswith(description_suffix):
            return _retrieve_stitch_infos_file(path)

    return []


def print_info(path: Path) -> None:
    if not path.exists():
        _error_not_exists(path)
        return

    descriptions = _retrieve_stitch_infos(path.resolve())

    for description_path, description in descriptions:
        _info_description(description_path, description)
