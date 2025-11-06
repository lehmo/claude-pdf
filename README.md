# PDF to iCloud Drive Mover

Scripts to move PDF files from your Downloads folder to your iCloud Drive "!PCC Reading and Other" folder.

## Prerequisites

- macOS with iCloud Drive enabled and synced
- A folder named "!PCC Reading and Other" in your iCloud Drive
- PDF files in your Downloads folder

## Usage

### Option 1: Python Script (Recommended)

```bash
python3 move_pdfs_to_icloud.py
```

### Option 2: Bash Script

```bash
chmod +x move_pdfs_to_icloud.sh
./move_pdfs_to_icloud.sh
```

## What These Scripts Do

1. Automatically locate your iCloud Drive folder
2. Find all PDF files in your Downloads folder
3. Move them to "!PCC Reading and Other" in iCloud Drive
4. Skip files that already exist in the destination (no overwriting)
5. Provide a summary of what was moved

## Safety Features

- No files are overwritten - existing files are skipped
- Clear output showing what's happening
- Error handling for missing folders
- Summary report at the end

## Troubleshooting

**"iCloud Drive folder not found"**
- Ensure iCloud Drive is enabled in System Preferences > Apple ID > iCloud
- Wait for iCloud Drive to finish syncing

**"Target folder not found"**
- Create the folder "!PCC Reading and Other" in your iCloud Drive
- Make sure the folder name matches exactly (including the exclamation mark)

**"No PDF files found"**
- Check that you have PDF files in your Downloads folder
- PDFs in subfolders won't be moved (only top-level PDFs)
