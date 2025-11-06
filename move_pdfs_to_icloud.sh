#!/bin/bash
# Script to move PDF files from Downloads to iCloud Drive folder
# Usage: ./move_pdfs_to_icloud.sh

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Find iCloud Drive path
if [ -d "$HOME/Library/Mobile Documents/com~apple~CloudDocs" ]; then
    ICLOUD_PATH="$HOME/Library/Mobile Documents/com~apple~CloudDocs"
elif [ -d "$HOME/iCloud Drive" ]; then
    ICLOUD_PATH="$HOME/iCloud Drive"
else
    echo -e "${RED}Error: iCloud Drive folder not found!${NC}"
    echo "Please ensure iCloud Drive is enabled and synced."
    exit 1
fi

# Target folder
TARGET_FOLDER="$ICLOUD_PATH/!PCC Reading and Other"

# Check if target folder exists
if [ ! -d "$TARGET_FOLDER" ]; then
    echo -e "${RED}Error: Target folder not found: $TARGET_FOLDER${NC}"
    echo "Please create the folder '!PCC Reading and Other' in your iCloud Drive."
    exit 1
fi

# Downloads folder
DOWNLOADS_FOLDER="$HOME/Downloads"

# Check if Downloads folder exists
if [ ! -d "$DOWNLOADS_FOLDER" ]; then
    echo -e "${RED}Error: Downloads folder not found!${NC}"
    exit 1
fi

# Count PDF files
PDF_COUNT=$(find "$DOWNLOADS_FOLDER" -maxdepth 1 -type f -name "*.pdf" | wc -l | tr -d ' ')

if [ "$PDF_COUNT" -eq 0 ]; then
    echo "No PDF files found in Downloads folder."
    exit 0
fi

echo "Found $PDF_COUNT PDF file(s) in Downloads:"
echo ""

MOVED_COUNT=0
SKIPPED_COUNT=0

# Move each PDF file
while IFS= read -r pdf_file; do
    filename=$(basename "$pdf_file")
    destination="$TARGET_FOLDER/$filename"

    echo "Processing: $filename"

    if [ -f "$destination" ]; then
        echo -e "  ${YELLOW}⚠️  File already exists in destination, skipping${NC}"
        ((SKIPPED_COUNT++))
    else
        if mv "$pdf_file" "$destination"; then
            echo -e "  ${GREEN}✓ Moved to iCloud Drive${NC}"
            ((MOVED_COUNT++))
        else
            echo -e "  ${RED}✗ Error moving file${NC}"
            ((SKIPPED_COUNT++))
        fi
    fi
done < <(find "$DOWNLOADS_FOLDER" -maxdepth 1 -type f -name "*.pdf")

# Summary
echo ""
echo "============================================================"
echo "SUMMARY"
echo "============================================================"
echo "Total PDFs found: $PDF_COUNT"
echo "Successfully moved: $MOVED_COUNT"
echo "Skipped: $SKIPPED_COUNT"
echo ""
echo "Files are now in: $TARGET_FOLDER"
