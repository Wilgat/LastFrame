# LastFrame

## Overview

LastFrame is a simple command-line tool for extracting the last frame from MP4 video files using OpenCV (cv2), providing multiple fallback methods for reliable frame seeking even with varying codecs or formats. It scans the current directory for MP4 files (case-insensitive), lists them with file sizes, allows interactive selection, and saves the frame as an image (PNG by default, supporting JPG, JPEG, BMP, TIFF). As a Cython (CyMaster type) project, it optimizes video capture and frame reading operations through compiled extensions for faster performance in media analysis tasks  . The tool includes user-friendly prompts, error handling for invalid videos, and pauses for result review, making it suitable for quick thumbnail generation or endpoint inspection without full video processing  .

## Features

- Automatic discovery of MP4 files in the current directory using glob patterns (handles case variations like .mp4, .MP4).
- Interactive numbered list display with file sizes in MB for easy selection.
- Robust last-frame extraction: Primary method uses frame count seeking; fallbacks include time-ratio (99%) and millisecond positioning for accuracy across videos.
- Flexible output naming: Defaults to "output.png" or "{video_stem}_last.png"; auto-appends image extension if missing.
- Success/failure feedback with method details (e.g., "using frame count").
- Cython compilation support for performance gains in OpenCV interactions, generating architecture-specific binaries like InstallPip.cpython-312-x86_64-linux-gnu.so equivalents for LastFrame  .
- No temporary files; direct save via cv2.imwrite with resource cleanup (cap.release()).

## Prerequisites

- Python 3.6+ (recommend 3.12; use pyenv for management: `curl https://pyenv.run | bash`, add to `~/.bashrc`, then `pyenv install 3.12.0` and `pyenv shell 3.12.0` for isolation) .
- OpenCV: Installed via pip (see Installation).
- C compiler (gcc on Linux/macOS, MSVC on Windows) for Cython builds.
- Git for repository management (recommended: `git init` to start tracking changes, excluding artifacts)   .

For development, create a virtual environment: `python3 -m venv venv; source venv/bin/activate` (Windows: `venv\Scripts\activate`) to avoid global conflicts .

## Installation

### From Source (Recommended for Development)

1. Clone or download the repository:
   ```
   git clone <repo-url>
   cd LastFrame
   ```

2. Initialize Git if needed (for version control):
   ```
   git init
   ```
     .

3. Configure `.gitignore` to exclude build artifacts, caches, and environment files:
   ```
   # .gitignore content
   .env
   __pycache__/
   *.pyc
   *.pyo
   *.so
   build/
   ```
   This keeps the repo clean, ignoring compiled modules like LastFrame.cpython-312-x86_64-linux-gnu.so    .

4. Create `requirements.txt` for dependencies (example):
   ```
   opencv-python
   ChronicleLogger
   cython  # For builds
   ```
   Install them:
   ```
   pip3 install -r requirements.txt
   ```
   Ensures reproducible setup across environments   .

5. Build and install in editable mode (compiles Cython extensions):
   ```
   # Install Cython if not in requirements
   pip install cython

   # Run build script (POSIX-compliant)
   chmod +x build.sh
   ./build.sh  # e.g., cythonize src/LastFrame/cli.pyx and python -m build

   # Editable install
   pip install -e .
   ```
   This generates outputs in `build/lib/` (e.g., LastFrame.cpython-310-arm-linux-gnueabihf.so for ARM) and makes the package importable  .

### Via pip (Packaged Release)

For the published version on PyPI:
```
pip3 install LastFrame
```
This installs OpenCV and other dependencies automatically, setting up the entry point for `python -m LastFrame`   .

Commit initial setup:
```
git add .
git commit -m "Initial commit"
```
 .

## Usage

### Command-Line Execution

Place MP4 files in the current directory and run:
```
python -m src.LastFrame
```
Or after installation:
```
python -m LastFrame
```
(Configure console_scripts in `pyproject.toml` for a `lastframe` command if desired.)

Example interactive session:
```
Found MP4 videos:

  1. sample.mp4  (23.5 MB)
  2. demo.MP4  (8.2 MB)

Enter video number (1-2): 1

Selected: sample.mp4
Enter output image filename [default: output.png]: end_frame.jpg

Extracting last frame from 'sample.mp4'...
Success: Last frame saved as 'end_frame.jpg'

Done! Image saved as: end_frame.jpg

Press Enter to exit...
```
The tool pauses at the end for viewing results .

For scripting, import and call: `from LastFrame.cli import main; main()` .

### Building for Distribution

- Use `python -m build` (via `pyproject.toml`) to create wheels/sdists.
- Outputs go to `build/` (gitignore them); supports architectures like x86_64-linux-gnu or arm-linux-gnueabihf  .

## Project Structure

The structure follows Cython best practices for maintainability, with `src/` isolating code, `docs/` for specifications, and `build/` for artifacts (excluded via .gitignore). Create folders with `mkdir -p docs src/LastFrame tests` if extending   .

```
LastFrame/
├── build.sh                  # Build script for Cython (e.g., cythonize and setup.py build_ext --inplace)
├── docs/                     # Documentation and specs
│   ├── CHANGELOG.md
│   ├── folder-structure.md
│   └── LastFrame-spec.md
├── pyproject.toml            # Build config with Cython directives (language_level=3)
├── README.md                 # This file
└── src/
    └── LastFrame/
        ├── cli.py            # CLI logic: glob discovery, selection, extraction
        ├── __init__.py       # Package init (exposes ChronicleLogger; rename suggested)
        └── __main__.py       # Entry point
```
Add `tests/` for validation (e.g., `touch tests/test_cli.py`) and `docs/update-log.md` for extended notes  .

## Development

- **Extensions**: Add batch support or more formats by modifying glob in `cli.py` (preserve existing code with `# NEW:` comments).
- **Testing**: Install pytest via requirements.txt; run `pytest tests/` to validate cv2 mocks.
- **Versioning**: Update `__version__` in `__init__.py` and CHANGELOG.md; use semantic releases.
- **Logging**: Integrate ChronicleLogger for traceable outputs (currently imported but unused).
- Touch additional files like `backend/app/main.py` or `tests/test_main.py` for modular growth, following patterns like `touch requirements.txt`   .

## Troubleshooting

- **OpenCV Import Error**: Run `pip3 install opencv-python`; verify with `python3 -c "import cv2"`.
- **Video Open Failure**: Ensure MP4 integrity; test with `cv2.VideoCapture('file.mp4').isOpened()`.
- **Cython Build Issues**: Check Python version (`which python3`); set `language_level=3` in pyproject.toml; use pyenv for consistency .
- **Permissions**: `chmod +x build.sh` on Unix; virtualenv avoids conflicts.
- No video found? Verify `os.getcwd()` and file extensions.

For issues, reference `docs/LastFrame-spec.md` or open a Git issue after `git init`  .

## License

MIT License (add LICENSE file with standard MIT text for open-source distribution) .