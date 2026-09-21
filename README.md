# smart-file-organizer

A simple Python script that automatically organizes your Downloads folder by sorting files into categorized subfolders (Images, Documents, Videos, etc.) based on file type.

## Features

- Automatically detects each file's type by its extension.
- Creates destination folders (e.g. `Images`, `Documents`) if they don't already exist.
- If a file with the same name already exists in the destination, the new file is automatically renamed (e.g. `photo.jpg` → `photo (1).jpg`) instead of being skipped or overwritten.
- Works on any machine automatically — it finds your Downloads folder based on your current user, no need to edit any paths.

## Requirements

- Python 3.6+
- No external libraries — only uses Python's built-in `pathlib` module.

## Usage

```bash
python file_organizer.py
```

The script will scan your `Downloads` folder and sort every file it finds into the matching subfolder.

## Notes

- Only files directly inside `Downloads` are organized; existing subfolders are left untouched.
- The extension-to-category mapping is defined in the `categories` dictionary at the top of the script — feel free to edit it to add or remove extensions/categories.
