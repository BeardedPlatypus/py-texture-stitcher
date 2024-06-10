<p align='center'><img align='center' src='https://github.com/BeardedPlatypus/py-texture-stitcher/blob/main/.docs/icon.png?raw=true' width='33%'></p>

# `sbe_stitch`

[![Linters](https://github.com/BeardedPlatypus/py-texture-stitcher/actions/workflows/linters.yml/badge.svg)](https://github.com/BeardedPlatypus/py-texture-stitcher/actions/workflows/linters.yml)
[![License](https://img.shields.io/github/license/BeardedPlatypus/py-texture-stitcher)](/LICENSE.md)

`sbe_stitch.exe` is a tiny CLI texture stitching application written in Python and provided as a single executable through [pyinstaller][pyinstaller].
Currently, it provides the ability to stich (similarly sized) images into a grid such that it can be consumed by Godot's `Texture2DArray` and
similar applications.

## Installation

The latest `sbe_stitch.exe` can be obtained from [the releases page](https://github.com/BeardedPlatypus/py-texture-stitcher/releases/latest).
Alternatively, the application can be installed through [scoop][scoop] by running the following:

```powershell
scoop bucket add scoop-bucket-tools https://github.com/BeardedPlatypus/scoop-bucket-tools
scoop install scoop-bucket-tools/sbe_stitch
```

Note that name `scoop-bucket-tools` can be replaced with another bucket name.

## Usage

Once installed, the help text can be printed by calling:

```powershell
sbe_stitch --help
```

It will provide a full overview of the commands. In addition, per command help information can be printed with:

```powershell
sbe_stitch <command-name> --help
```

Currently, the following two commands are available:

* `info`: print the stitch description of the provided stitched file, or any stitched files in the provided directory.
* `stitch`: stitch the images in the provided location into a single file.

## Attribution

* <a href="https://www.flaticon.com/free-icons/tailoring" title="tailoring icons">Tailoring icons created by Freepik - Flaticon</a>

[pyinstaller]: https://pyinstaller.org/en/stable/
[scoop]: https://scoop.sh/
