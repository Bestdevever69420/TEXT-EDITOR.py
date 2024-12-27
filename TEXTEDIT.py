import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import platform
import subprocess

class SystemThemedTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        
        # Detect system theme and apply
        self.current_theme = self.detect_system_theme()
        self.apply_theme(self.current_theme)

        # Create text area
        self.text_area = tk.Text(self.root, wrap="word", undo=True, bg=self.bg_color, fg=self.fg_color, insertbackground=self.fg_color)
        self.text_area.pack(expand=1, fill="both")
        self.text_area.bind("<KeyRelease>", self.update_word_count)

        # Create word count label
        self.word_count_label = tk.Label(self.root, text="Words: 0")
        self.word_count_label.pack(side="bottom", anchor="e")

        # Add menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.root.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.root.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.root.event_generate("<<Paste>>"))
        edit_menu.add_command(label="Find and Replace", command=self.open_find_replace_dialog)
        edit_menu.add_command(label="Change Font", command=self.change_font)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # File path
        self.file_path = None

        # Default font
        self.font_family = "Arial"
        self.font_size = 12
        self.text_area.config(font=(self.font_family, self.font_size))

    def detect_system_theme(self):
        system = platform.system()
        try:
            if system == "Windows":
                import winreg as reg
                key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                value, _ = reg.QueryValueEx(key, "AppsUseLightTheme")
                return "light" if value == 1 else "dark"
            elif system == "Darwin":  # macOS
                result = subprocess.run(["defaults", "read", "-g", "AppleInterfaceStyle"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return "dark" if "Dark" in result.stdout.decode() else "light"
            elif system == "Linux":
                # Example for GNOME
                result = subprocess.run(["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                theme = result.stdout.decode().strip().lower()
                return "dark" if "dark" in theme else "light"
        except Exception:
            return "light"  # Default to light theme if detection fails

    def apply_theme(self, theme):
        if theme == "dark":
            self.bg_color = "#2E2E2E"
            self.fg_color = "#FFFFFF"
        else:
            self.bg_color = "#FFFFFF"
            self.fg_color = "#000000"

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.update_word_count()

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())
            self.file_path = file_path
            self.root.title(f"Text Editor - {file_path}")
            self.update_word_count()

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.file_path = file_path
            self.root.title(f"Text Editor - {file_path}")

    def show_about(self):
        messagebox.showinfo("About", "System-Themed Text Editor made with Python and Tkinter")

    def update_word_count(self, event=None):
        text = self.text_area.get(1.0, tk.END)
        words = len(text.split())
        self.word_count_label.config(text=f"Words: {words}")

    def open_find_replace_dialog(self):
        find_replace_dialog = tk.Toplevel(self.root)
        find_replace_dialog.title("Find and Replace")
        find_replace_dialog.geometry("300x150")

        tk.Label(find_replace_dialog, text="Find:").grid(row=0, column=0, padx=10, pady=5)
        self.find_entry = tk.Entry(find_replace_dialog, width=20)
        self.find_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(find_replace_dialog, text="Replace:").grid(row=1, column=0, padx=10, pady=5)
        self.replace_entry = tk.Entry(find_replace_dialog, width=20)
        self.replace_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(find_replace_dialog, text="Find", command=self.find_text).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(find_replace_dialog, text="Replace", command=self.replace_text).grid(row=2, column=1, padx=10, pady=5)

    def find_text(self):
        self.text_area.tag_remove("highlight", "1.0", tk.END)
        search_text = self.find_entry.get()
        if search_text:
            start_pos = "1.0"
            while True:
                start_pos = self.text_area.search(search_text, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_text)}c"
                self.text_area.tag_add("highlight", start_pos, end_pos)
                start_pos = end_pos
            self.text_area.tag_config("highlight", background="yellow", foreground="black")

    def replace_text(self):
        search_text = self.find_entry.get()
        replace_text = self.replace_entry.get()
        if search_text and replace_text:
            content = self.text_area.get("1.0", tk.END)
            new_content = content.replace(search_text, replace_text)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", new_content)
            self.update_word_count()

    def change_font(self):
        font_family = simpledialog.askstring("Font", "Enter font family:", initialvalue=self.font_family)
        font_size = simpledialog.askinteger("Font", "Enter font size:", initialvalue=self.font_size)
        if font_family and font_size:
            self.font_family = font_family
            self.font_size = font_size
            self.text_area.config(font=(self.font_family, self.font_size))

if __name__ == "__main__":
    root = tk.Tk()
    editor = SystemThemedTextEditor(root)
    root.geometry("800x600")
    root.mainloop()
import keyword

class SystemThemedTextEditor:
    # ... (other methods remain unchanged)

    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        
        # Detect system theme and apply
        self.current_theme = self.detect_system_theme()
        self.apply_theme(self.current_theme)

        # Create text area
        self.text_area = tk.Text(self.root, wrap="word", undo=True, bg=self.bg_color, fg=self.fg_color, insertbackground=self.fg_color)
        self.text_area.pack(expand=1, fill="both")
        self.text_area.bind("<KeyRelease>", self.update_word_count)
        self.text_area.bind("<KeyRelease>", self.highlight_syntax)

        # Create word count label
        self.word_count_label = tk.Label(self.root, text="Words: 0")
        self.word_count_label.pack(side="bottom", anchor="e")

        # Add menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.root.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.root.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.root.event_generate("<<Paste>>"))
        edit_menu.add_command(label="Find and Replace", command=self.open_find_replace_dialog)
        edit_menu.add_command(label="Change Font", command=self.change_font)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # File path
        self.file_path = None

        # Default font
        self.font_family = "Arial"
        self.font_size = 12
        self.text_area.config(font=(self.font_family, self.font_size))

        # Configure tags for syntax highlighting
        self.text_area.tag_configure("keyword", foreground="blue")
        self.text_area.tag_configure("string", foreground="green")
        self.text_area.tag_configure("comment", foreground="gray")

    def highlight_syntax(self, event=None):
        self.text_area.tag_remove("keyword", "1.0", tk.END)
        self.text_area.tag_remove("string", "1.0", tk.END)
        self.text_area.tag_remove("comment", "1.0", tk.END)

        text = self.text_area.get("1.0", tk.END)
        lines = text.split("\n")

        for i, line in enumerate(lines):
            index = f"{i + 1}.0"
            for token in line.split():
                if token in keyword.kwlist:
                    start = line.find(token)
                    end = start + len(token)
                    self.text_area.tag_add("keyword", f"{i + 1}.{start}", f"{i + 1}.{end}")
                elif token.startswith("#"):
                    start = line.find(token)
                    self.text_area.tag_add("comment", f"{i + 1}.{start}", f"{i + 1}.end")
                    break
                elif token.startswith(("'", '"')) and token.endswith(("'", '"')):
                    start = line.find(token)
                    end = start + len(token)
                    self.text_area.tag_add("string", f"{i + 1}.{start}", f"{i + 1}.{end}")

    # ... (other methods remain unchanged)
