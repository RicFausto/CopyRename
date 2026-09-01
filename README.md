# A small desktop app (built with Python/tkinter) for batch-copying files with custom names and folder organization.

[]

## What it does:

**Select files** — choose one or more files from anywhere on your computer.

**Build a rename pattern** — combine tokens (Name, Year, Month, Day, Time, Counter) with your own custom text to generate new filenames. A live preview shows the old name next to the new one for every file before you commit.

**Preview** — a table lists every file and exactly what it'll be renamed to.

**Copy to a destination** — pick any folder on disk. Optionally, set a subfolder pattern (using the same tokens, e.g. Year/Year-Month) to automatically sort copies into nested folders like 2026/2026-08 — created if they don't exist, reused if they do. Leave it blank to copy files straight into the destination.

Files are copied, not moved, and original metadata (timestamps) is preserved on the copies. The app runs standalone with no internet connection or external accounts needed.
