# Copy & Rename

A small desktop app for batch-copying files with custom names and automatic folder organization. Built with Python's built-in `tkinter`, so there's nothing extra to install to run it from source.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

### 👉 [Download the latest version](https://github.com/RicFausto/CopyRename/releases/latest)

## Features

- **Select multiple files** at once via a native file picker.
- **Token-based renaming** — build new filenames from file metadata and your own custom text:
  - `Name` — original filename (without extension)
  - `Year`, `Month`, `Day` — from the file's last-modified date
  - `Time` — last-modified time (`HHMMSS`)
  - `Counter` — zero-padded sequence number
  - `Custom` — your own free-text input
- **Live preview** — see every original name next to its new name before copying anything.
- **Automatic subfolder organization** — optionally sort copies into nested folders built from the same tokens (e.g. `Year/Year-Month` → `2026/2026-08`). Folders are created if they don't exist, and reused if they do.
- **Metadata-preserving copies** — uses `shutil.copy2`, so timestamps are preserved on the copies. Files are copied, never moved or altered.
- **No external dependencies, no network access** — everything runs locally.

## Requirements

- Python 3.8 or later
- `tkinter` (bundled with most Python installs; on some Linux distros install separately, e.g. `sudo apt install python3-tk`)

## Usage

```bash
python copy_rename_app.py
```

1. **Choose files** — click "Select files…" and pick one or more files.
2. **Build the rename pattern** — enter custom text and a pattern (default: `YearMonthDay-Time-Custom`), using the token buttons to insert placeholders. The preview table updates live.
3. **Choose a destination folder.**
4. *(Optional)* **Set a subfolder path** — e.g. `Year/Year-Month` — to sort copies into nested folders automatically. Leave blank to copy files directly into the destination.
5. Click **Copy renamed files**.

## Building a standalone executable

You can package the app into a single `.exe` (Windows), `.app` (macOS), or standalone binary (Linux) using [PyInstaller](https://pyinstaller.org/), so it can run on machines without Python installed.

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name CopyRename copy_rename_app.py
```

The executable will be in the generated `dist/` folder.

> **Note:** PyInstaller builds are platform-specific — build on Windows to get a `.exe`, on macOS to get a `.app`, etc.

## License

MIT — feel free to use, modify, and distribute.
