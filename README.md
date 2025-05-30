# Download Organizer

A simple and efficient tool to organize your downloads folder by automatically sorting files into appropriate categories.

## Features

- Automatically organizes files into categories (Images, PDFs, Documents, Archives, Executables, and Others)
- Prevents duplicate files by adding number suffixes
- Simple and intuitive GUI interface
- Automatic update system
- Works with existing folders without creating duplicates

## Installation

1. Download the latest release from the [Releases](https://github.com/hamzahharist/download-organizer/releases) page
2. Run the `Download Organizer.exe` file
3. No installation required - it's a portable application

## Usage

1. Launch the application
2. The default folder is set to your Downloads folder
3. Click "Browse" to select a different folder if needed
4. Click "Organize Now" to start organizing files
5. Click "Check for Updates" to manually check for new versions

## File Categories

- **Images**: .png, .jpg, .jpeg, .gif, .bmp, .svg
- **PDFs**: .pdf
- **Documents**: .doc, .docx, .xls, .xlsx, .ppt, .pptx, .txt
- **Archives**: .zip, .rar, .7z, .tar, .gz
- **Executables**: .exe, .msi, .bat, .sh
- **Others**: All other file types

## Development

### Requirements

- Python 3.11 or higher
- Required packages:
  - tkinter
  - requests

### Building from source

1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Build the executable: `pyinstaller --onefile --windowed --name "Download Organizer" download_manager.py`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
