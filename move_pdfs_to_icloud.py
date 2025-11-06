#!/usr/bin/env python3
"""
Script to move PDF files from Downloads to iCloud Drive folder.
This script safely moves PDF files from your Downloads folder to
iCloud Drive's "!PCC Reading and Other" folder.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def find_icloud_drive():
    """Find the iCloud Drive path."""
    home = Path.home()
    possible_paths = [
        home / "Library" / "Mobile Documents" / "com~apple~CloudDocs",
        home / "iCloud Drive",
    ]

    for path in possible_paths:
        if path.exists():
            return path

    return None

def main():
    # Find Downloads folder
    downloads_folder = Path.home() / "Downloads"

    if not downloads_folder.exists():
        print("Error: Downloads folder not found!")
        return

    # Find iCloud Drive
    icloud_drive = find_icloud_drive()

    if not icloud_drive:
        print("Error: iCloud Drive folder not found!")
        print("Please ensure iCloud Drive is enabled and synced.")
        return

    # Target folder
    target_folder = icloud_drive / "!PCC Reading and Other"

    if not target_folder.exists():
        print(f"Error: Target folder not found: {target_folder}")
        print("Please create the folder '!PCC Reading and Other' in your iCloud Drive.")
        return

    # Find all PDF files in Downloads
    pdf_files = list(downloads_folder.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in Downloads folder.")
        return

    print(f"Found {len(pdf_files)} PDF file(s) in Downloads:")
    print()

    moved_files = []
    skipped_files = []

    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")

        destination = target_folder / pdf_file.name

        # Check if file already exists
        if destination.exists():
            print(f"  ⚠️  File already exists in destination, skipping: {pdf_file.name}")
            skipped_files.append(pdf_file.name)
            continue

        try:
            # Move the file
            shutil.move(str(pdf_file), str(destination))
            print(f"  ✓ Moved to iCloud Drive")
            moved_files.append(pdf_file.name)
        except Exception as e:
            print(f"  ✗ Error moving file: {e}")
            skipped_files.append(pdf_file.name)

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total PDFs found: {len(pdf_files)}")
    print(f"Successfully moved: {len(moved_files)}")
    print(f"Skipped: {len(skipped_files)}")
    print()

    if moved_files:
        print("Moved files:")
        for filename in moved_files:
            print(f"  - {filename}")

    if skipped_files:
        print()
        print("Skipped files:")
        for filename in skipped_files:
            print(f"  - {filename}")

    print()
    print(f"Files are now in: {target_folder}")

if __name__ == "__main__":
    main()
