# Copy & Rename

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

A small desktop app for batch-copying files with custom names and automatic folder organization. 

The app runs standalone with no internet connection or external accounts needed.

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
