# Peek-A-Boo

Fast, lightweight file previews on Linux — without launching full editing applications.

Peek-A-Boo is designed for quick inspection of files directly from the terminal or file manager, making it easy to “peek” at contents and move on without breaking flow.

Peek-A-Boo started as a way to avoid waiting for full applications to load when all I needed was a quick glance.

## Screenshots

![Peek-A-Boo spreadsheet called from terminal](assets/images/screenshots/spreadsheet_preview_from_commandline.png)

## How it works (high level)

1. A file path is passed to Peek-A-Boo (via terminal command or keyboard shortcut)
2. Peek-A-Boo generates a lightweight preview instead of loading the entire file
3. The preview is displayed using simple, see-what-you-need tooling
4. Generated previews are cached to enable near-instant repeat viewing

## Features

- Fast previews without opening full applications
- Partial rendering to minimize startup time
- Preview caching for near-instant repeat access
- Designed for terminal and keyboard-driven workflows

## Supported File Types

- Spreadsheets (initial support)

## Caching Behavior

- Previews are cached for 30 minutes by default
- Cached previews are reused if the source file has not changed
- Cached previews display almost instantly
- Cache duration is configurable

## Quick Start

1. Install dependencies:
   ```
   ./scripts/install_dependencies.sh
   ```
2. Run Peek-A-Boo:
   ```
   python3 peekaboo_thumbnail_with_cache.py <file>
   ```
3. Optionally bind the script to a keyboard shortcut or file manager action

## Requirements

- feh
- libreoffice

## Roadmap / In Development

- Add support for additional file types:
    - Audio
    - Video
    - Images
    - Documents
    - Presentations
- Helper script for file manager and keyboard shortcut integration

