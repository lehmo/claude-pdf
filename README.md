# PDF to iCloud Drive Mover

Scripts to move PDF files from your Downloads folder to your iCloud Drive "!PCC Reading and Other" folder.

## Features

- **Smart Book Detection**: Verifies PDFs are actual books (50+ pages, has author/title or ISBN)
- **Safe Moving**: No overwrites - skips files that already exist
- **Detailed Reports**: Shows what was moved and why files were skipped
- **Multiple Options**: Simple one-liners or full-featured Python scripts

## Prerequisites

- macOS with iCloud Drive enabled and synced
- A folder named "!PCC Reading and Other" in your iCloud Drive
- PDF files in your Downloads folder
- For smart book detection: Python 3 with `pypdf` library

## Recommended: Smart Book Verification Script

This script only moves PDFs that are actual books (50+ pages with author/title or ISBN):

### 1. Install dependencies:
```bash
pip3 install pypdf
```

### 2. Run the script:
```bash
python3 move_book_pdfs.py
```

**What it checks:**
- ✓ At least 50 pages
- ✓ Has author AND title metadata, OR
- ✓ Has ISBN number

**Output example:**
```
📄 Sapiens.pdf
   ✓ Book verified: Author: Yuval Noah Harari, Title: Sapiens
   📖 464 pages
   ➜ Moved to iCloud Drive

📄 tax-form-2023.pdf
   ❌ Not a book: Only 12 pages (need 50+)
```

## Quick One-Liners (Move ALL PDFs)

If you want to move all PDFs without verification:

### Basic version:
```bash
for pdf in ~/Downloads/*.pdf; do [ -f "$pdf" ] && mv -n "$pdf" ~/Library/Mobile\ Documents/com~apple~CloudDocs/\!PCC\ Reading\ and\ Other/ && echo "Moved: $(basename "$pdf")"; done
```

### With summary:
```bash
echo "Moving PDFs..." && moved=0 && for pdf in ~/Downloads/*.pdf; do [ -f "$pdf" ] && mv -n "$pdf" ~/Library/Mobile\ Documents/com~apple~CloudDocs/\!PCC\ Reading\ and\ Other/ && echo "✓ $(basename "$pdf")" && ((moved++)); done && echo "Done! Moved $moved file(s)"
```

## Other Scripts

### Move all PDFs (no verification):

**Python:**
```bash
python3 move_pdfs_to_icloud.py
```

**Bash:**
```bash
chmod +x move_pdfs_to_icloud.sh
./move_pdfs_to_icloud.sh
```

## Safety Features

- No files are overwritten - existing files are skipped
- Clear output showing what's happening
- Error handling for missing folders
- Summary report at the end

## How Book Verification Works

The smart script (`move_book_pdfs.py`) checks each PDF for:

1. **Page Count**: Must have at least 50 pages
2. **Metadata**: Must have either:
   - Author AND Title in PDF metadata, OR
   - ISBN number (checked in metadata and first 3 pages)

**Examples of what gets moved:**
- ✓ Academic books with proper metadata
- ✓ eBooks from publishers (usually have ISBN)
- ✓ Technical books and textbooks

**Examples of what gets skipped:**
- ❌ Short documents, forms, receipts
- ❌ Presentations and reports (unless 50+ pages with metadata)
- ❌ Scanned documents without metadata

## Troubleshooting

**"pypdf not found"**
```bash
pip3 install pypdf
```

**"iCloud Drive folder not found"**
- Ensure iCloud Drive is enabled in System Preferences > Apple ID > iCloud
- Wait for iCloud Drive to finish syncing

**"Target folder not found"**
- Create the folder "!PCC Reading and Other" in your iCloud Drive
- Make sure the folder name matches exactly (including the exclamation mark)

**"No PDF files found"**
- Check that you have PDF files in your Downloads folder
- PDFs in subfolders won't be moved (only top-level PDFs)

**PDF has metadata but was skipped:**
- Check if it has at least 50 pages
- Verify metadata with: `python3 -c "from pypdf import PdfReader; r = PdfReader('file.pdf'); print(r.metadata)"`
