# LastFrame

## Overview

**LastFrame** is a lightweight command-line tool that extracts the **first frame** from MP4 video files using OpenCV (`cv2`).  

It automatically scans the current directory for `.mp4` files (case-insensitive), displays an interactive numbered list with file sizes, lets the user select a video, and saves the first frame as an image file (PNG by default; supports JPG, JPEG, BMP, TIFF).  

The tool features clear prompts, basic error handling, and a pause at the end — perfect for quick thumbnail generation, cover image creation, or inspecting video starts without loading the entire file.

## Features

- Finds all `.mp4` / `.MP4` / `.Mp4` files in the current folder using `glob`
- Shows numbered list with file sizes (in MB) for easy selection
- Extracts the very first frame reliably with a single `cap.read()` call
- Smart default output filename: `output.png` (if free) or `{video_name}_first.png`
- Automatically adds `.png` extension if user input lacks an image suffix
- Clean resource handling (`cap.release()`) — no temporary files
- User-friendly success/error messages and final confirmation

## Prerequisites

- Python 3.8+ (recommended: 3.10–3.12)
- `opencv-python` (installed via pip)
- Optional: virtual environment (`venv` or `uv`)

No C compiler or Cython is required for normal usage — the project is currently pure Python.

## Installation

### Development / Source Install (Editable)

```bash
# 1. Clone or download the repo
git clone <your-repo-url>
cd LastFrame

# 2. (Recommended) Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install opencv-python
# If you later add ChronicleLogger or others → add them here

# 4. Install project in editable mode
pip install -e .
```

Now you can run it with:

```bash
python -m LastFrame
```

### Future PyPI Release (when ready)

```bash
pip install lastframe
```

(You would then publish it via `python -m build` + twine, and configure `console_scripts` in `pyproject.toml` for a `lastframe` command.)

## Usage

Place your MP4 videos in the current directory and run:

```bash
python -m LastFrame
```

Example session:

```
Found MP4 videos:

  1. intro.mp4   (12.4 MB)
  2. demo.MP4    (45.8 MB)

Enter video number (1-2): 1

Selected: intro.mp4
Enter output image filename [default: output.png]: 

Extracting first frame from 'intro.mp4'...
Success: First frame saved as 'output.png'

Done! Image saved as: output.png

Press Enter to exit...
```

Or specify a custom name:

```
Enter output image filename [default: intro_first.png]: cover.jpg
```

The tool saves the image and waits for you to press Enter before closing.

For scripting / automation:

```python
from LastFrame.__main__ import main
main()
```

## Project Structure

Follows modern Python packaging conventions with `src/` layout:

```
LastFrame/
├── README.md
├── pyproject.toml            # (add when packaging properly)
├── src/
│   └── LastFrame/
│       ├── __init__.py
│       └── __main__.py       # Main logic + entry point
└── (optional future folders)
    ├── tests/
    └── docs/
```

## Development Notes

- The core logic lives in `src/LastFrame/__main__.py`
- To add features (batch mode, other formats, progress bar…): edit the `main()` and `get_first_frame()` functions
- Logging: `ChronicleLogger` is imported but unused — either integrate it or remove the import
- Tests: Consider adding `tests/` folder + `pytest` later
- Packaging: When ready, add `pyproject.toml` with `build-system = {requires = ["hatchling"], build-backend = "hatchling.build"}` (or setuptools)

## Troubleshooting

- **Cannot open video** → Check file path, integrity, and codec support in your OpenCV build
- **No MP4 files found** → Make sure videos are in the current working directory (`pwd`)
- **OpenCV not found** → `pip install opencv-python`
- **Permission denied on save** → Check write permissions in current folder

## License

MIT License  
(Add a `LICENSE` file with the standard MIT text when you publish or share the repo.)
