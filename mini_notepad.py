import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import font as tkfont


class TextEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Untitled - Mini Notepad")
        self.geometry("900x600")

        self.current_file = None
        self.unsaved_changes = False
        self.dark_mode = False

        self.current_font_family = "Consolas"
        self.current_font_size = 12
        self.text_font = tkfont.Font(family=self.current_font_family, size=self.current_font_size)

        self._create_widgets()
        self._create_menu()
        self._bind_shortcuts()

    # ---------------- GUI SETUP ---------------- #
    def _create_widgets(self):
        # Main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar + Text widget
        self.text_scroll = tk.Scrollbar(self.main_frame)
        self.text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = tk.Text(
            self.main_frame,
            wrap="word",
            undo=True,
            yscrollcommand=self.text_scroll.set,
            font=self.text_font
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.text_scroll.config(command=self.text_area.yview)

        # Track modifications for save prompts and status bar
        self.text_area.bind("<<Modified>>", self._on_text_modified)

        # Status bar for word/character count
        self.status_bar = tk.Label(self, text="Words: 0  Chars: 0", anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Window close protocol
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def _create_menu(self):
        self.menu_bar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_exit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Search menu (Find/Replace)
        search_menu = tk.Menu(self.menu_bar, tearoff=0)
        search_menu.add_command(label="Find / Replace", command=self.open_find_replace, accelerator="Ctrl+F")
        self.menu_bar.add_cascade(label="Search", menu=search_menu)

        # View menu (Dark mode)
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_checkbutton(label="Dark Mode", command=self.toggle_dark_mode)
        self.menu_bar.add_cascade(label="View", menu=view_menu)

        # Format menu (Font size)
        format_menu = tk.Menu(self.menu_bar, tearoff=0)
        format_menu.add_command(label="Increase Font Size", command=lambda: self.change_font_size(2))
        format_menu.add_command(label="Decrease Font Size", command=lambda: self.change_font_size(-2))
        format_menu.add_command(label="Set Font Size...", command=self.set_font_size_dialog)
        self.menu_bar.add_cascade(label="Format", menu=format_menu)

        self.config(menu=self.menu_bar)

    def _bind_shortcuts(self):
        self.bind("<Control-n>", lambda event: self.new_file())
        self.bind("<Control-o>", lambda event: self.open_file())
        self.bind("<Control-s>", lambda event: self.save_file())
        self.bind("<Control-S>", lambda event: self.save_file_as())  # Ctrl+Shift+S
        self.bind("<Control-a>", lambda event: self.select_all())
        self.bind("<Control-f>", lambda event: self.open_find_replace())

    # ---------------- FILE OPERATIONS ---------------- #
    def new_file(self):
        if not self._confirm_discard_changes():
            return
        self.text_area.delete("1.0", tk.END)
        self.current_file = None
        self.unsaved_changes = False
        self._update_title()
        self._update_status_bar()

    def open_file(self):
        if not self._confirm_discard_changes():
            return

        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")
            return

        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", content)
        self.current_file = file_path
        self.unsaved_changes = False
        self._update_title()
        self._update_status_bar()
        self.text_area.edit_modified(False)

    def save_file(self):
        if self.current_file is None:
            return self.save_file_as()

        try:
            content = self.text_area.get("1.0", tk.END)
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(content.rstrip("\n"))
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")
            return

        self.unsaved_changes = False
        self._update_title()
        self.text_area.edit_modified(False)

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            content = self.text_area.get("1.0", tk.END)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content.rstrip("\n"))
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")
            return

        self.current_file = file_path
        self.unsaved_changes = False
        self._update_title()
        self.text_area.edit_modified(False)

    # ---------------- EDIT / SEARCH FEATURES ---------------- #
    def select_all(self):
        self.text_area.tag_add("sel", "1.0", tk.END)
        return "break"

    def open_find_replace(self):
        FindReplaceDialog(self, self.text_area)

    # ---------------- VIEW / FORMAT FEATURES ---------------- #
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            bg = "#1e1e1e"
            fg = "#ffffff"
            insert_bg = "#ffffff"
            status_bg = "#2d2d2d"
        else:
            bg = "#ffffff"
            fg = "#000000"
            insert_bg = "#000000"
            status_bg = self.cget("bg")

        self.text_area.config(bg=bg, fg=fg, insertbackground=insert_bg)
        self.status_bar.config(bg=status_bg, fg=fg if self.dark_mode else "#000000")

    def change_font_size(self, delta):
        new_size = max(6, self.current_font_size + delta)
        self.current_font_size = new_size
        self.text_font.configure(size=new_size)

    def set_font_size_dialog(self):
        try:
            size = simpledialog.askinteger("Font Size", "Enter font size:", minvalue=6, maxvalue=72, parent=self)
        except Exception:
            size = None
        if size:
            self.current_font_size = size
            self.text_font.configure(size=size)

    # ---------------- STATUS / MODIFICATION HANDLING ---------------- #
    def _on_text_modified(self, event=None):
        if self.text_area.edit_modified():
            self.unsaved_changes = True
            self._update_title()
            self._update_status_bar()
            self.text_area.edit_modified(False)

    def _update_title(self):
        if self.current_file:
            name = self.current_file.split("/")[-1].split("\\")[-1]
        else:
            name = "Untitled"
        if self.unsaved_changes:
            self.title(f"*{name} - Mini Notepad")
        else:
            self.title(f"{name} - Mini Notepad")

    def _update_status_bar(self):
        text = self.text_area.get("1.0", "end-1c")
        chars = len(text)
        words = len(text.split()) if text.strip() else 0
        self.status_bar.config(text=f"Words: {words}  Chars: {chars}")

    def _confirm_discard_changes(self):
        if not self.unsaved_changes:
            return True
        response = messagebox.askyesnocancel("Unsaved Changes", "Do you want to save changes?")
        if response is None:
            return False  # Cancel
        if response:
            self.save_file()
            # If still unsaved (e.g. save was cancelled), do not proceed
            return not self.unsaved_changes
        return True

    def on_exit(self):
        if not self._confirm_discard_changes():
            return
        self.destroy()


class FindReplaceDialog(tk.Toplevel):
    def __init__(self, parent, text_widget: tk.Text):
        super().__init__(parent)
        self.title("Find / Replace")
        self.resizable(False, False)
        self.text_widget = text_widget

        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(self, text="Replace with:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.find_entry = tk.Entry(self, width=30)
        self.replace_entry = tk.Entry(self, width=30)
        self.find_entry.grid(row=0, column=1, padx=5, pady=5)
        self.replace_entry.grid(row=1, column=1, padx=5, pady=5)

        find_button = tk.Button(self, text="Find Next", command=self.find_next)
        replace_button = tk.Button(self, text="Replace", command=self.replace_one)
        replace_all_button = tk.Button(self, text="Replace All", command=self.replace_all)
        close_button = tk.Button(self, text="Close", command=self.destroy)

        find_button.grid(row=0, column=2, padx=5, pady=5)
        replace_button.grid(row=1, column=2, padx=5, pady=5)
        replace_all_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")
        close_button.grid(row=2, column=2, padx=5, pady=5)

        self.bind("<Return>", lambda event: self.find_next())

        # Tag for highlighting search results
        self.text_widget.tag_config("search_highlight", background="yellow", foreground="black")

    def _clear_highlight(self):
        self.text_widget.tag_remove("search_highlight", "1.0", tk.END)

    def find_next(self):
        pattern = self.find_entry.get()
        if not pattern:
            return

        self._clear_highlight()

        start = self.text_widget.index(tk.INSERT)
        pos = self.text_widget.search(pattern, start, stopindex=tk.END, nocase=True)

        if not pos:
            messagebox.showinfo("Find", "No more matches found.")
            return

        end = f"{pos}+{len(pattern)}c"
        self.text_widget.tag_add("search_highlight", pos, end)
        self.text_widget.mark_set(tk.INSERT, end)
        self.text_widget.see(pos)

    def replace_one(self):
        pattern = self.find_entry.get()
        replacement = self.replace_entry.get()
        if not pattern:
            return

        self._clear_highlight()

        start = self.text_widget.index(tk.INSERT)
        pos = self.text_widget.search(pattern, start, stopindex=tk.END, nocase=True)

        if not pos:
            messagebox.showinfo("Replace", "No match found.")
            return

        end = f"{pos}+{len(pattern)}c"
        self.text_widget.delete(pos, end)
        self.text_widget.insert(pos, replacement)
        self.text_widget.mark_set(tk.INSERT, f"{pos}+{len(replacement)}c")
        self.text_widget.see(pos)

    def replace_all(self):
        pattern = self.find_entry.get()
        replacement = self.replace_entry.get()
        if not pattern:
            return

        count = 0
        start = "1.0"
        self._clear_highlight()

        while True:
            pos = self.text_widget.search(pattern, start, stopindex=tk.END, nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(pattern)}c"
            self.text_widget.delete(pos, end)
            self.text_widget.insert(pos, replacement)
            start = f"{pos}+{len(replacement)}c"
            count += 1

        messagebox.showinfo("Replace All", f"Replaced {count} occurrence(s).")


if __name__ == "__main__":
    app = TextEditor()
    app.mainloop()
