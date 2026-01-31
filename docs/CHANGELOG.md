# CHANGELOG

## [1.0.0] - 2026-01-31
### Added
- Core functionality for extracting the last frame from MP4 videos using OpenCV (cv2) with multiple seek methods: frame count positioning, AVI ratio fallback, and millisecond seeking for reliability .
- Interactive CLI interface: glob-based discovery of MP4 files (case-insensitive), sorted list display with file sizes, user selection prompts, and default output naming logic .
- Package structure with `cli.py` for main logic, `__init__.py` exposing version and components (e.g., ChronicleLogger import), and `__main__.py` for entry point execution .
- Error handling for video capture failures and input validation, including pauses for user review via `input()` .
- Cython build support through `build.sh` and `pyproject.toml` for compiling performance-critical sections like VideoCapture operations .

### Changed
- Initial implementation uses procedural functions; potential future OOP refactor to a `LastFrameExtractor` class without modifying existing code .

### Deprecated
- None in initial release.

### Removed
- None.

### Fixed
- Robust fallback mechanisms address common OpenCV seek inaccuracies for variable-length videos, ensuring frame extraction success rates across codecs .
- Deduplication and sorting of glob results prevent display errors for mixed-case filenames .

### Security
- Safe file path handling via `os.path` and `cv2.VideoCapture`; no direct user input injection into system calls, with validation for output extensions .

---

This CHANGELOG follows semantic versioning and reverse chronological order for clear project evolution tracking, using categorized sections (Added, Changed, Deprecated, Removed, Fixed, Security) to communicate updates concisely to users and contributors    . Update sections as changes occur, maintaining consistent formatting for readability .