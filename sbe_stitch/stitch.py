import json
import math
from pathlib import Path
from typing import Optional, Sequence, Tuple

from PIL import Image
from PIL.Image import Image as PILImage
from rich import print
from rich.padding import Padding

from sbe_stitch import common
from sbe_stitch.description import Dimension, StitchDescription, SUFFIX


# TODO: * Add support for specifying specific file paths
#       * Add support for updating existing stitches with new images
def _retrieve_image_paths(input_directory: Path) -> Sequence[Path]:
    return list(input_directory.glob("*.png"))


def _error_inconsistent_size(images: Sequence[Tuple[Path, PILImage]]) -> None:
    common.error("Inconsistent sizes found:")
    for p, img in images:
        print(Padding(f"{p.resolve()}: {img.size}", (0, 0, 0, 4)))


def _retrieve_images(
    input_directory: Path,
) -> Optional[Sequence[Tuple[Path, PILImage]]]:
    if not input_directory.exists():
        common.error(f"The input folder '{input_directory}' does not exist.")
        return None
    if not input_directory.is_dir():
        common.error(f"The input folder '{input_directory}' is not a directory.")
        return None

    image_paths = _retrieve_image_paths(input_directory)

    if not image_paths:
        common.error(f"No images found in the input folder '{input_directory}'.")
        return None

    images = [(p, Image.open(p)) for p in image_paths]

    expected_size = images[0][1].size
    if any((img.size != expected_size for _, img in images[1:])):
        _error_inconsistent_size(images)
        return None

    return images


def _determine_dimensions(n_images: int) -> Tuple[int, int]:
    a_float = int(math.ceil(math.sqrt(n_images)))
    b_float = int(math.ceil(n_images / a_float))
    return a_float, b_float


def _is_valid_dimensions(preferred_dimensions: Tuple[int, int], n_images: int) -> bool:
    return preferred_dimensions[0] * preferred_dimensions[1] >= n_images


def _error_incorrect_stitch_dimensions(
    preferred_dimensions: Tuple[int, int], n_images: int
) -> None:
    common.error(
        f"The preferred dimension '{preferred_dimensions}' supports fewer images "
        f"that the found images, '{n_images}'"
    )


def _calculate_stitch_image_size(
    img_size: Tuple[int, int], stitch_dimensions: Tuple[int, int]
) -> Tuple[int, int]:
    return img_size[0] * stitch_dimensions[0], img_size[1] * stitch_dimensions[1]


def _stitch(
    images: Sequence[Tuple[Path, PILImage]], stitch_dimensions: Tuple[int, int]
) -> Tuple[PILImage, StitchDescription]:
    elem_img_size = images[0][1].size
    new_image_size = _calculate_stitch_image_size(elem_img_size, stitch_dimensions)
    stitch_img = Image.new("RGBA", new_image_size)

    for i, (_, img) in enumerate(images):
        x_i = i % stitch_dimensions[0]
        y_i = i // stitch_dimensions[0]

        img_pos = (x_i * elem_img_size[0], y_i * elem_img_size[1])
        stitch_img.paste(img, img_pos)

    description = StitchDescription(
        [p for p, _ in images],
        Dimension(stitch_dimensions[0], stitch_dimensions[1]),
        Dimension(elem_img_size[0], elem_img_size[1]),
    )

    return stitch_img, description


def _write_description(file_path: Path, description: StitchDescription) -> None:
    data = description.to_dict()
    with file_path.open("w") as fp:
        json.dump(data, fp, indent=4)


def _success_stitched_image(output_path_img: Path, output_path_description: Path) -> None: 
    common.success("Stitched image:")
    print(Padding(f"Image: {output_path_img}", (0, 0, 0, 4)))
    print(Padding(f"Description: {output_path_description}", (0, 0, 0, 4)))


def stitch(
    output_path: Path,
    input_directory: Path,
    dims: Optional[Tuple[int, int]],
) -> None:
    if not (images := _retrieve_images(input_directory)):
        return

    if dims and not _is_valid_dimensions(dims, len(images)):
        _error_incorrect_stitch_dimensions(dims, len(images))
        return

    dimensions = dims or _determine_dimensions(len(images))

    stitched_image, stitched_description = _stitch(images, dimensions)

    if output_path.exists() and output_path.is_dir():
        output_path = output_path / f"{output_path.name}.png"

    output_path_description = output_path.with_suffix(SUFFIX)

    _write_description(output_path_description, stitched_description)
    stitched_image.save(output_path)

    _success_stitched_image(output_path, output_path_description)
