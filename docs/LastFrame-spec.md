# Design Document for `LastFrame`

## Overview

The `LastFrame` project is a command-line utility designed to extract the final frame from MP4 video files using OpenCV (cv2) for precise frame seeking and image saving, supporting multiple fallback methods to ensure reliability across varying video formats and codecs. As a Cython (CyMaster type) project, it optimizes performance-critical operations like video capture and frame reading through compiled extensions, targeting media processing workflows where quick thumbnail or endpoint image extraction is needed without full video decoding   . The tool scans the current directory for MP4 files (case-insensitive), displays them with file sizes, allows interactive selection, suggests output filenames, and handles image saving in formats like PNG, JPG, or BMP. It includes robust error handling for video opening failures and user input validation, promoting maintainability in production environments via Cython's seamless integration with Python libraries like OpenCV   . The project adheres to CyMaster conventions for structure and build, facilitating compilation into standalone executables for cross-platform distribution  .

## Target Operating System

The project targets cross-platform use, with primary focus on Unix-like systems (Linux, macOS) due to the shebang `#!/usr/bin/env python` and POSIX-compatible paths via `glob` and `os`. It supports Windows through OpenCV's compatibility, but requires adjustments for PATH resolution and executable builds. For Cython compilation, it relies on C compilers (e.g., gcc on Linux/macOS, MSVC on Windows) to generate binaries or `.so` modules, ensuring seamless integration in diverse environments. The `build.sh` script provides POSIX-compliant automation for compilation, while `pyproject.toml` configures tools like setuptools and Cython for wheel distribution, enhancing maintainability without heavy dependencies    .

## Folder Structure

The folder structure follows CyMaster conventions for Cython projects, separating source code, documentation, and build configurations to support compilation into standalone executables or shared libraries, with git-friendly organization for version control and easy management of directory layouts    . It includes dedicated docs for specifications and changelogs, src isolation for modularity, and build automation to generate binaries in subfolders like `build/bin/amd64-glibc/` for architecture-specific outputs, promoting robust documentation and cross-platform compatibility  .

```
LastFrame/
├── build.sh                  # POSIX-compliant shell script for Cython compilation, e.g., cythonize and build_ext (compatible with CentOS 6+ environments)
├── docs/
│   ├── CHANGELOG.md          # Release notes tracking additions like fallback methods or OpenCV optimizations
│   ├── folder-structure.md   # Explanation of layout, including rationale for CyMaster-style src/ and build/ separation
│   └── LastFrame-spec.md     # Project specifications: supported formats (MP4 only), OpenCV dependencies, Cython directives (e.g., language_level=3)
├── pyproject.toml            # Build configuration for setuptools/Cython, defining ext_modules for cli.pyx compilation and metadata
├── README.md                 # User guide with installation, usage examples, and prerequisite setup
└── src/
    └── LastFrame/
        ├── cli.py            # Core CLI logic: file discovery via glob, interactive selection, frame extraction with cv2
        ├── __init__.py       # Package initialization: exposes ChronicleLogger (recommend rename to LastFrameExtractor for alignment) and version
        └── __main__.py       # Entry point: imports and executes main() from cli.py for direct invocation
```

This layout facilitates the Directory Tree Structure Generator for enhanced documentation, ensuring easy compilation to executables and exclusion of artifacts via `.gitignore` (e.g., `__pycache__/`, `build/bin/*`)    .

### Parameters

- **Video Formats**: Limited to MP4 (case-insensitive via glob: `*.mp4`, `*.MP4`, `*.Mp4`); sorted alphabetically after deduplication .
- **Output Defaults**: "output.png" if not existing, else `{video_stem}_last.png`; auto-appends ".png" if no image extension provided (supports PNG, JPG, JPEG, BMP, TIFF) .
- **Frame Extraction Methods**:
  - Primary: Set `cv2.CAP_PROP_POS_FRAMES` to `total_frames - 1` for exact last frame.
  - Fallback 1: `cv2.CAP_PROP_POS_AVI_RATIO` at 0.99 (time-based seek).
  - Fallback 2: `cv2.CAP_PROP_POS_MSEC` to ~0.1s before end, using FPS and duration calculation.
- **Dependencies**: Requires OpenCV (cv2) via pip (`pip install opencv-python`); standard library (sys, os, glob); no FFmpeg needed. For Cython, include `compiler_directives={'language_level': 3}` in setup  .
- **User Interaction**: Numbered list with file sizes (MB); loop for valid input (1 to N); pauses with `input()` for console visibility.
- **Cython-Specific**: Convert `cli.py` to `.pyx` for compiling performance bottlenecks like `VideoCapture` loops; `build.sh` automates `cythonize -i src/LastFrame/cli.pyx` and `python -m build`   .

## Project Name Conversion Rules

- **Package Name**: `LastFrame` (CamelCase for module/directory, per PEP 8 and CyMaster norms).
- **File Naming**: Snake_case for Python files (e.g., `cli.py`); descriptive lowercase for docs (e.g., `LastFrame-spec.md`).
- **Output Files**: User-specified or default `{stem}_last.png` (preserves video stem, adds "_last" for clarity; image extensions enforced).
- **Temporary/Intermediates**: None explicit; Cython builds produce `.c`, `.so`, or executables prefixed with `LastFrame_` (e.g., `LastFrame_cli.cpython-312-x86_64-linux-gnu.so`) in `build/bin/` subdirs like `amd64-glibc/` or `armv7l-glibc/`   .
- **Versioning**: Semantic (`__version__ = "1.0.0"` in `__init__.py`); track via CHANGELOG.md and cy-master.ini if extended for builds  .
- **Build Artifacts**: Use lowercase paths without spaces; architecture-specific folders (e.g., `amd64-glibc/`) for binaries to ensure cross-platform compatibility .

Adhere to safe, portable naming to avoid issues in compilation and distribution  .

## Class Structure

The current implementation uses procedural functions in `cli.py`, with no explicit classes, but `__init__.py` exposes `ChronicleLogger` (mismatch; suggest refactor to `LastFrameExtractor` class for OOP encapsulation). For Cython optimization, wrap extraction logic in a class to leverage typed memoryviews for frame handling, improving speed in video I/O  .

### Attributes

- None defined at instance level (functional paradigm). Package-level:
  - `__version__`: String "1.0.0" for semantic tracking.
  - `__all__`: List `["ChronicleLogger"]` (update to `["LastFrameExtractor", "main"]` post-refactor)  .

### Methods

#### Instance Methods

- No current instances; proposed `LastFrameExtractor` class for Cython refactor (append as `# NEW:` to preserve code):
  - `__init__(self, video_path: str) -> None`: Initializes `cv2.VideoCapture` for the selected file.
  - `extract_last_frame(self, output_path: str) -> bool`: Orchestrates frame seeking methods (POS_FRAMES primary, fallbacks); saves via `cv2.imwrite`; returns success.
  - `get_video_info(self) -> Dict[str, Any]`: Retrieves properties like `CAP_PROP_FRAME_COUNT`, `CAP_PROP_FPS` for diagnostics  .
  - `cleanup(self) -> None`: Releases capture (`cap.release()`) to free resources.

These additions would maintain existing functions intact, compiling to efficient extensions for OpenCV interactions  .

## Functionality Supported

- **File Discovery**: Glob-based search for MP4s in current directory (`os.getcwd()`); deduplicates and sorts; displays with indices and sizes (MB via `os.path.getsize()`) .
- **Interactive Selection**: Validates numeric input in loop; handles empty/invalid choices with prompts.
- **Frame Extraction**: Robust cv2.VideoCapture with three seek methods for last frame reliability (frame count preferred for accuracy); saves as image with success messages.
- **Output Management**: Default naming logic; extension appending; supports multiple image formats.
- **Error Handling**: Checks `cap.isOpened()`; prints failures; pauses for user review (`input()`); no temp files needed.
- **Cython Enhancements**: Compile for faster frame reading (e.g., cdef functions for cv2 calls); `build.sh` and `pyproject.toml` enable standalone executables in `build/bin/`, with support for architectures like amd64-glibc and armv7l-glibc    .
- **Extensibility**: Modular for adding formats (e.g., AVI via glob extension) or batch extraction; integrate logging via ChronicleLogger if aligned  .

Supports simple, isolated use without deployment overhead, scalable via tests/ addition for validation  .

## Usage Example

1. **Setup**: Place MP4 files in the run directory. Install OpenCV: `pip install opencv-python` (use venv: `python3 -m venv venv; source venv/bin/activate`).

2. **Run Directly**:
   ```
   python -m src.LastFrame
   ```
   Or post-build: `./build/bin/amd64-glibc/LastFrame` (after `build.sh`).

3. **Interactive Session Example**:
   ```
   Found MP4 videos:

     1. video1.mp4  (45.2 MB)
     2. video2.MP4  (12.8 MB)

   Enter video number (1-2): 1

   Selected: video1.mp4
   Enter output image filename [default: output.png]: video1_end.jpg

   Extracting last frame from 'video1.mp4'...
   Success: Last frame saved as 'video1_end.jpg' (using frame count)

   Done! Image saved as: video1_end.jpg

   Press Enter to exit...
   ```

4. **Cython Build** (via `build.sh`, POSIX-compliant):
   ```
   # Example build.sh snippet:
   # ===== BEGIN NEW CODE =====
   # NEW: cythonize -i src/LastFrame/cli.pyx
   # NEW: python -m build --wheel
   # NEW: # Outputs to build/bin/amd64-glibc/LastFrame executable
   # ===== END NEW CODE =====
   chmod +x build.sh
   ./build.sh
   pip install -e .  # For development
   ```
   Generates architecture-specific binaries for distribution    .

5. **Package Install**: Future PyPI: `pip3 install LastFrame`; runs as `python -m LastFrame` .

For maintenance, update CHANGELOG.md per releases and use `.gitignore` for `build/*`, `__pycache__/`; add `tests/` with pytest for cv2 mocking .