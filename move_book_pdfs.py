#!/usr/bin/env python3
"""
Script to move book PDFs from Downloads to iCloud Drive folder.
This script verifies PDFs are actually books before moving them by checking:
- At least 50 pages
- Has author and title metadata OR ISBN
"""

import os
import re
import shutil
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("Error: This script requires pypdf or PyPDF2.")
        print("Install with: pip3 install pypdf")
        exit(1)


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


def extract_isbn(text):
    """Extract ISBN from text if present."""
    if not text:
        return None

    # ISBN-13 pattern
    isbn13_pattern = r'(?:ISBN(?:-13)?:?\s*)?(?=[-0-9 ]{17}|[0-9]{13})(?:97[89][-\s]?)?[0-9]{1,5}[-\s]?[0-9]+[-\s]?[0-9]+[-\s]?[0-9]'
    # ISBN-10 pattern
    isbn10_pattern = r'(?:ISBN(?:-10)?:?\s*)?(?=[-0-9X ]{13}|[0-9X]{10})[0-9]{1,5}[-\s]?[0-9]+[-\s]?[0-9]+[-\s]?[0-9X]'

    match = re.search(isbn13_pattern, text, re.IGNORECASE) or re.search(isbn10_pattern, text, re.IGNORECASE)
    return match.group() if match else None


def is_book_pdf(pdf_path, min_pages=50):
    """
    Check if a PDF is likely a book by verifying:
    1. Has at least min_pages pages
    2. Has author and title metadata OR ISBN

    Returns: (is_book, reason, details_dict)
    """
    try:
        reader = PdfReader(str(pdf_path))
        page_count = len(reader.pages)

        # Check page count
        if page_count < min_pages:
            return False, f"Only {page_count} pages (need {min_pages}+)", {"pages": page_count}

        # Extract metadata
        metadata = reader.metadata if reader.metadata else {}

        # Get metadata fields (handle None values)
        author = metadata.get('/Author', '') or ''
        title = metadata.get('/Title', '') or ''
        subject = metadata.get('/Subject', '') or ''

        # Clean metadata strings
        author = str(author).strip()
        title = str(title).strip()
        subject = str(subject).strip()

        # Check for ISBN in metadata
        isbn = extract_isbn(subject) or extract_isbn(title)

        # Try to find ISBN in first few pages
        if not isbn and page_count > 0:
            try:
                # Check first 3 pages for ISBN
                for i in range(min(3, page_count)):
                    page_text = reader.pages[i].extract_text()
                    isbn = extract_isbn(page_text)
                    if isbn:
                        break
            except:
                pass

        details = {
            "pages": page_count,
            "author": author,
            "title": title,
            "isbn": isbn
        }

        # Book criteria: (author AND title) OR isbn
        has_author_and_title = bool(author) and bool(title)
        has_isbn = bool(isbn)

        if has_author_and_title or has_isbn:
            reason = []
            if has_author_and_title:
                reason.append(f"Author: {author[:50]}, Title: {title[:50]}")
            if has_isbn:
                reason.append(f"ISBN: {isbn}")
            return True, " | ".join(reason), details
        else:
            missing = []
            if not author:
                missing.append("author")
            if not title:
                missing.append("title")
            if not isbn:
                missing.append("ISBN")
            return False, f"Missing: {', '.join(missing)}", details

    except Exception as e:
        return False, f"Error reading PDF: {str(e)}", {}


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

    print(f"Found {len(pdf_files)} PDF file(s) in Downloads")
    print(f"Checking which ones are books (50+ pages with metadata)...\n")
    print("=" * 80)

    moved_books = []
    skipped_not_books = []
    skipped_errors = []
    skipped_exists = []

    for pdf_file in pdf_files:
        print(f"\n📄 {pdf_file.name}")

        # Check if it's a book
        is_book, reason, details = is_book_pdf(pdf_file)

        if not is_book:
            print(f"   ❌ Not a book: {reason}")
            skipped_not_books.append((pdf_file.name, reason))
            continue

        print(f"   ✓ Book verified: {reason}")
        print(f"   📖 {details['pages']} pages")

        # Check if already exists
        destination = target_folder / pdf_file.name
        if destination.exists():
            print(f"   ⚠️  Already exists in destination")
            skipped_exists.append(pdf_file.name)
            continue

        # Move the file
        try:
            shutil.move(str(pdf_file), str(destination))
            print(f"   ➜ Moved to iCloud Drive")
            moved_books.append((pdf_file.name, details))
        except Exception as e:
            print(f"   ✗ Error moving: {e}")
            skipped_errors.append((pdf_file.name, str(e)))

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total PDFs found: {len(pdf_files)}")
    print(f"Books moved: {len(moved_books)}")
    print(f"Not books (skipped): {len(skipped_not_books)}")
    print(f"Already exist: {len(skipped_exists)}")
    print(f"Errors: {len(skipped_errors)}")

    if moved_books:
        print(f"\n✓ MOVED BOOKS ({len(moved_books)}):")
        for filename, details in moved_books:
            print(f"  • {filename}")
            if details.get('author'):
                print(f"    Author: {details['author']}")
            if details.get('title'):
                print(f"    Title: {details['title']}")
            print(f"    Pages: {details['pages']}")

    if skipped_not_books:
        print(f"\n❌ SKIPPED (Not books - {len(skipped_not_books)}):")
        for filename, reason in skipped_not_books:
            print(f"  • {filename}")
            print(f"    Reason: {reason}")

    if skipped_exists:
        print(f"\n⚠️  SKIPPED (Already exist - {len(skipped_exists)}):")
        for filename in skipped_exists:
            print(f"  • {filename}")

    if skipped_errors:
        print(f"\n✗ ERRORS ({len(skipped_errors)}):")
        for filename, error in skipped_errors:
            print(f"  • {filename}: {error}")

    print(f"\n📁 Target folder: {target_folder}")


if __name__ == "__main__":
    main()
