"""
Smart File Organizer
---------------------
Scans the Downloads folder and automatically sorts every file into a
subfolder based on its file extension (e.g. .jpg -> Images, .pdf -> Documents).

If a file with the same name already exists in the destination folder,
the script automatically renames the new file (e.g. "photo.jpg" ->
"photo (1).jpg") instead of overwriting or crashing.
"""

from pathlib import Path


def get_unique_path(target_path: Path) -> Path:
    """
    Given a desired file path, return a path that is guaranteed not to
    already exist.

    - If target_path doesn't exist yet, it's returned as-is.
    - If it does exist, we keep trying "name (1).ext", "name (2).ext", ...
      until we find a name that isn't taken.

    This prevents FileExistsError when two different files share the same
    name (e.g. two files both called "photo.jpg" downloaded on different days).
    """
    if not target_path.exists():
        return target_path

    counter = 1
    while True:
        # Build a candidate name like "photo (1).jpg"
        new_name = f"{target_path.stem} ({counter}){target_path.suffix}"
        new_path = target_path.parent / new_name

        if not new_path.exists():
            return new_path

        counter += 1


# Maps each category (destination folder name) to the list of file
# extensions that belong to it. Extensions must be lowercase here,
# since we lowercase the file's extension before comparing (see below).
categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".csv", ".odt", ".rtf"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".wma"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Programs": [".exe", ".msi", ".apk", ".dmg", ".pkg"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".java", ".cpp", ".c", ".php", ".sql", ".xml", ".ts"],
    "Ebooks": [".epub", ".mobi", ".azw3"],
    "Fonts": [".ttf", ".otf", ".woff"],
}

# Path to the folder we want to organize.
# The r"..." prefix (raw string) stops Python from treating backslashes
# as escape characters (e.g. \n, \t) inside the Windows path.
Downloads_folder = Path.home() / "Downloads"
# Go through every item directly inside the Downloads folder.
for f in Downloads_folder.iterdir():

    # Skip subfolders - we only want to move actual files.
    if f.is_file():

        # Lowercase the extension so "Photo.JPG" and "photo.jpg" are
        # treated the same way when matched against `categories`.
        file_extension = f.suffix.lower()

        # Check every category to see if this file's extension belongs to it.
        for category, extensions in categories.items():
            if file_extension in extensions:
                category_folder = Downloads_folder / category

                # Create the destination folder if it doesn't exist yet.
                # exist_ok=True means "don't raise an error if it's already there".
                category_folder.mkdir(exist_ok=True)

                # Move the file, auto-renaming it if a same-named file
                # already exists in the destination folder.
                f.rename(get_unique_path(category_folder / f.name))

                # We found the right category - no need to check the rest.
                break

        else:
            # This `else` belongs to the `for` loop above (not to an `if`).
            # It only runs if the loop finished WITHOUT hitting `break`,
            # meaning the file's extension didn't match any known category.
            other_folder = Downloads_folder / "Others"
            other_folder.mkdir(exist_ok=True)
            f.rename(get_unique_path(other_folder / f.name))