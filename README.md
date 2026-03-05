# Mini Notepad (Python Tkinter Text Editor)

Mini Notepad is a simple text editor desktop application built with Python and Tkinter. It mimics the basic functionality of Notepad, allowing you to create, open, edit, and save plain text files, with a few extra usability features.

## Features

- **GUI with Tkinter**
  - Resizable window
  - Main text area with vertical scrollbar

- **File operations**
  - **New**: Clear the editor to start a new document
  - **Open**: Open existing `.txt` or any text file
  - **Save**: Save changes to the current file
  - **Save As**: Save the document as a new file
  - **Exit**: Quit the application
  - Window title shows the **current file name** (or `Untitled`)
  - Unsaved changes are indicated with a leading `*` in the window title
  - Prompts you to **save changes** before New/Open/Exit if the document was modified

- **Edit operations**
  - Cut
  - Copy
  - Paste
  - Select All

- **Search & Replace**
  - Find next occurrence (case-insensitive)
  - Replace single occurrence
  - Replace all occurrences with a counter message

- **View / Theme**
  - Optional **Dark Mode** toggle (View → Dark Mode)

- **Format / Font**
  - Increase font size
  - Decrease font size
  - Set custom font size via dialog

- **Status Bar**
  - Live **word count**
  - Live **character count**

- **Keyboard Shortcuts**
  - `Ctrl + N` – New file
  - `Ctrl + O` – Open file
  - `Ctrl + S` – Save file
  - `Ctrl + Shift + S` – Save As
  - `Ctrl + A` – Select All
  - `Ctrl + F` – Find / Replace

## Project Structure

```text
notepad/
├── mini_notepad.py   # Main application
└── README.md         # Project documentation
```

## Requirements

- Python 3.x
- Tkinter (usually included with standard Python installations on Windows)

## How to Run

1. Clone or download this repository.
2. Open a terminal in the project folder (where `mini_notepad.py` is located).
3. Run the application:

   ```bash
   python mini_notepad.py
   ```

On Windows PowerShell, for example:

```powershell
cd "C:\Users\bhara\OneDrive\Desktop\notepad"
python mini_notepad.py
```

## Usage Overview

- Use the **File** menu to create, open, save, or exit.
- Use the **Edit** menu for basic text editing operations.
- Use the **Search → Find / Replace** menu (or `Ctrl + F`) to search within the document and optionally replace text.
- Toggle **Dark Mode** from the **View** menu for a darker theme.
- Adjust font size from the **Format** menu.
- Watch the bottom status bar for live word and character counts.

## Possible Future Enhancements

- Line numbers in a gutter next to the text area
- Font family selection (e.g., switch between Consolas, Courier New, etc.)
- Word wrap toggle and encoding options
- Recent files list
- Printing support

## License

This project is for learning and personal use. You are free to modify and extend it for your own projects.
