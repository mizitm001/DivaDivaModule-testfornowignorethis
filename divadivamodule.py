import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tkinter import PhotoImage
import csv
import os
import subprocess
import json
import sys
import shutil
from PIL import Image, ImageTk

# --- Default app data directory for everyone ---
def get_app_dir():
    return os.path.expanduser("~/.divadivamodule")

APP_DIR = get_app_dir()
NOTES_CSV = os.path.join(APP_DIR, "notes.csv")
MODULES_CSV = os.path.join(APP_DIR, "modules_data.csv")
SETTINGS_FILE = os.path.join(APP_DIR, "settings.json")
IMAGES_FOLDER = os.path.join(APP_DIR, "images")
# Define a dedicated items folder within the app directory
ITEMS_FOLDER = os.path.join(APP_DIR, "items") # Added ITEMS_FOLDER

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STARTER_MODULES_CSV = os.path.join(SCRIPT_DIR, "modules_data.csv")
SCRIPT_IMAGES_SOURCE_DIR = os.path.join(SCRIPT_DIR, "images")

# --- GLOBAL COLOR AND THEME DEFINITIONS ---
CHARACTER_COLORS = {
    "Miku": "#00eaff",
    "Len": "#fffb00",
    "Rin": "#ffae00",
    "Kaito": "#0800ff",
    "Meiko": "#ff0800",
    "Luka": "#f58ed3",
    "Teto": "#f70535",
    "Neru": "#ffe600",
    "Haku": "#dbcef2",
    "Sakine": "#572513"
}

THEMES = {
    'light': {
        'bg': '#ffffff',
        'fg': '#000000',
        'select_bg': '#dedede',
        'select_fg': '#ffffff',
        'entry_bg': '#ffffff',
        'entry_fg': '#000000',
        'button_bg': '#f0f0f0',
        'button_fg': '#000000',
        'frame_bg': '#f0f0f0',
        'listbox_bg': '#ffffff',
        'listbox_fg': '#000000',
        'tree_bg': '#ffffff',
        'tree_fg': '#000000'
    },
    'dark': {
        'bg': '#2d2d2d',
        'fg': '#ffffff',
        'select_bg': '#dedede',
        'select_fg': '#ffffff',
        'entry_bg': '#404040',
        'entry_fg': '#ffffff',
        'button_bg': '#404040',
        'button_fg': '#ffffff',
        'frame_bg': '#2d2d2d',
        'listbox_bg': '#404040',
        'listbox_fg': '#ffffff',
        'tree_bg': '#404040',
        'tree_fg': '#ffffff'
    }
}

class ThemeManager:
    def __init__(self):
        self.current_theme = "light"

    def load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    s = json.load(f)
                    self.current_theme = s.get('theme', self.current_theme)
        except Exception:
            pass

    def save_settings(self, settings_data=None): # Modified to accept settings_data
        try:
            if settings_data is None:
                # If no data is passed, load existing and update only theme
                settings_data = {}
                if os.path.exists(SETTINGS_FILE):
                    with open(SETTINGS_FILE, 'r') as f:
                        try:
                            settings_data = json.load(f)
                        except json.JSONDecodeError:
                            settings_data = {}

            settings_data['theme'] = self.current_theme # Always update theme

            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings_data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save theme settings: {e}")

    def get_theme(self):
        return THEMES[self.current_theme]

    def set_theme(self, theme_name):
        if theme_name in THEMES:
            self.current_theme = theme_name
            self.save_settings()

    def apply_theme_to_widget(self, widget, widget_type='default'):
        theme = self.get_theme()
        try:
            if widget_type == 'listbox':
                widget.configure(
                    bg=theme['listbox_bg'],
                    fg=theme['listbox_fg'],
                    selectbackground=theme['select_bg'],
                    selectforeground=theme['select_fg'],
                    highlightbackground=theme['bg'],
                    highlightcolor=theme['bg']
                )
            elif widget_type == 'entry':
                widget.configure(
                    bg=theme['entry_bg'],
                    fg=theme['entry_fg'],
                    insertbackground=theme['fg'],
                    highlightbackground=theme['bg'],
                    highlightcolor=theme['bg']
                )
            elif widget_type == 'button':
                widget.configure(
                    bg=theme['button_bg'],
                    fg=theme['button_fg'],
                    activebackground=theme['select_bg'],
                    activeforeground=theme['select_fg'],
                    highlightbackground=theme['bg'],
                    highlightcolor=theme['bg'],
                    borderwidth=0
                )
            elif widget_type == 'frame':
                widget.configure(bg=theme['frame_bg'], highlightbackground=theme['frame_bg'])
            elif widget_type == 'label':
                widget.configure(
                    bg=theme['bg'],
                    fg=theme['fg']
                )
            elif widget_type == 'toplevel':
                widget.configure(bg=theme['bg'])
            else:
                widget.configure(bg=theme['bg'])
                try:
                    widget.configure(fg=theme['fg'])
                except Exception:
                    pass
        except Exception:
            pass

    def apply_theme_to_treeview(self, tree):
        theme = self.get_theme()
        style = ttk.Style()
        treeview_style = f"{self.current_theme}.Treeview"
        heading_style = f"{self.current_theme}.Treeview.Heading"
        style.configure(
            treeview_style,
            background=theme['tree_bg'],
            foreground=theme['tree_fg'],
            fieldbackground=theme['tree_bg'],
            bordercolor=theme['frame_bg'],
            borderwidth=0,
            font=('Arial', 10)
        )
        style.map(
            treeview_style,
            background=[('selected', theme['select_bg'])],
            foreground=[('selected', theme['select_fg'])]
        )
        style.configure(
            heading_style,
            background=theme['button_bg'],
            foreground=theme['button_fg'],
            font=('Arial', 10, 'bold')
        )
        tree.configure(style=treeview_style)

    def apply_theme_to_combobox(self, combobox):
        theme = self.get_theme()
        style = ttk.Style()
        style_name = f"{self.current_theme}.TCombobox"
        style.configure(
            style_name,
            fieldbackground=theme['entry_bg'],
            background=theme['entry_bg'],
            foreground=theme['entry_fg'],
            selectbackground=theme['select_bg'],
            selectforeground=theme['select_fg'],
            bordercolor=theme['frame_bg'],
            arrowcolor=theme['fg']
        )
        combobox.configure(style=style_name)

    def apply_theme_to_separator(self, separator):
        theme = self.get_theme()
        style = ttk.Style()
        style_name = f"{self.current_theme}.TSeparator"
        style.configure(style_name, background=theme['fg'])
        separator.configure(style=style_name)

theme_manager = ThemeManager()


# --- Function Definitions ---

def ensure_app_structure():
    os.makedirs(APP_DIR, exist_ok=True)
    os.makedirs(IMAGES_FOLDER, exist_ok=True)
    os.makedirs(ITEMS_FOLDER, exist_ok=True) # Ensure ITEMS_FOLDER exists

    # Copy starter modules_data.csv if it doesn't exist in APP_DIR
    if not os.path.exists(MODULES_CSV):
        if os.path.exists(STARTER_MODULES_CSV):
            try:
                shutil.copyfile(STARTER_MODULES_CSV, MODULES_CSV)
                print(f"Copied starter modules_data.csv to {MODULES_CSV}")
            except Exception as e:
                print(f"Error copying starter modules_data.csv: {e}")
        else:
            with open(MODULES_CSV, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Module ID", "Name (EN)", "Name (JP)", "Character",
                    "Source", "COS ID", "Item ID", "Object(s)", "Type"
                ])
                print(f"Created empty {MODULES_CSV}")

    if not os.path.exists(NOTES_CSV):
        with open(NOTES_CSV, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
        print(f"Created empty {NOTES_CSV}")

    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({}, f)
        print(f"Created empty {SETTINGS_FILE}")

    # --- REVISED LOGIC: Copy character images ---
    print("Checking for character images to copy...")

    for char_name in CHARACTER_COLORS.keys():
        possible_fnames = [f"{char_name}.png"]
        if ' ' in char_name:
             possible_fnames.append(f"{char_name.lower().replace(' ', '_')}.png")

        copied_this_char = False
        for fname in possible_fnames:
            src_path = os.path.join(SCRIPT_IMAGES_SOURCE_DIR, fname)
            dest_path = os.path.join(IMAGES_FOLDER, fname)

            if os.path.isfile(src_path) and not os.path.exists(dest_path):
                try:
                    shutil.copyfile(src_path, dest_path)
                    print(f"Copied character image '{fname}' from '{SCRIPT_IMAGES_SOURCE_DIR}' to '{IMAGES_FOLDER}'")
                    copied_this_char = True
                    break
                except Exception as e:
                    print(f"Error copying character image '{fname}': {e}")
            elif not os.path.isfile(src_path):
                print(f"Source image '{fname}' not found in '{SCRIPT_IMAGES_SOURCE_DIR}'.")

        if not copied_this_char and not os.path.exists(os.path.join(IMAGES_FOLDER, f"{char_name}.png")):
             print(f"Image for '{char_name}' already exists in app directory or no suitable source found in '{SCRIPT_IMAGES_SOURCE_DIR}'.")
        elif not copied_this_char and os.path.exists(os.path.join(IMAGES_FOLDER, f"{char_name}.png")):
             print(f"Image for '{char_name}' already exists in app directory.")

    print("Finished checking/coping character images.")


def center_window(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() - width) // 2
    y = (win.winfo_screenheight() - height) // 2
    win.geometry(f"+{x}+{y}")

def first_launch_prompt():
    temp_root = tk.Tk()
    temp_root.withdraw()

    win = tk.Toplevel(temp_root)
    win.title("Welcome to DivaDivaModule!")
    win.geometry("440x300")
    win.grab_set()
    win.resizable(False, False)
    center_window(win)

    frame = tk.Frame(win)
    frame.pack(fill='both', expand=True, padx=20, pady=20)
    tk.Label(frame, text="Welcome to DivaDivaModule!", font=('Arial', 16, 'bold')).pack(pady=(0,10))
    tk.Label(frame, text="Let's set up your environment.").pack(pady=(0, 18))

    exe_var = tk.StringVar()
    wine_var = tk.StringVar()

    def browse_exe():
        path = filedialog.askopenfilename(title="Select MikuMikuModel.exe", filetypes=[("Exe files", "*.exe")])
        if path:
            exe_var.set(path)
    def browse_wine():
        path = filedialog.askdirectory(title="Select .wine prefix (optional)")
        if path:
            wine_var.set(path)

    exe_row = tk.Frame(frame)
    exe_row.pack(fill='x', pady=6)
    tk.Label(exe_row, text="MikuMikuModel.exe:", width=18, anchor='w').pack(side='left')
    exe_entry = tk.Entry(exe_row, textvariable=exe_var, width=38)
    exe_entry.pack(side='left', fill='x', expand=True)
    tk.Button(exe_row, text="Browse", command=browse_exe).pack(side='left')

    wine_row = tk.Frame(frame)
    wine_row.pack(fill='x', pady=6)
    tk.Label(wine_row, text="Wine Prefix (optional):", width=18, anchor='w').pack(side='left')
    wine_entry = tk.Entry(wine_row, textvariable=wine_var, width=38)
    wine_entry.pack(side='left', fill='x', expand=True)
    tk.Button(wine_row, text="Browse", command=browse_wine).pack(side='left')

    def confirm():
        exe = exe_var.get().strip()
        wine = wine_var.get().strip()

        if not exe or not os.path.isfile(exe):
            messagebox.showerror("Setup Error", "Please select a valid MikuMikuModel.exe.")
            return

        settings_to_save = {
            "mikumikumodel_exe": exe,
            "wineprefix": wine,
            "theme": "light"
        }

        try:
            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings_to_save, f, indent=4)

            messagebox.showinfo("Setup Complete", "Initial settings saved successfully.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save initial settings: {e}\nDirectory tried: {os.path.dirname(SETTINGS_FILE)}")

    tk.Button(frame, text="Save & Continue", command=confirm, font=('Arial', 11)).pack(pady=(24,0))

    win.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))

    temp_root.wait_window(win)

    # Destroy the temporary root window after the first launch prompt is done
    try:
        if temp_root.winfo_exists():
            temp_root.destroy()
    except Exception:
        pass


def load_settings():
    # If settings file doesn't exist, prompt for first launch setup
    if not os.path.exists(SETTINGS_FILE):
        first_launch_prompt()
    else:
        # If settings file exists, check its content
        with open(SETTINGS_FILE, "r") as f:
            try:
                s = json.load(f)
                # Check if mikumikumodel_exe is missing or invalid
                if "mikumikumodel_exe" not in s or not os.path.isfile(s["mikumikumodel_exe"]):
                    first_launch_prompt()
            except json.JSONDecodeError: # Handle empty or malformed JSON
                # If JSON is corrupt, treat it as first launch
                first_launch_prompt()
            except Exception: # Catch any other unexpected errors during loading
                first_launch_prompt()
    # Re-open the file after potential first_launch_prompt to ensure it's loaded
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

# --- Global Variables and Initial Setup ---
ensure_app_structure()

# Load settings after ensuring the app structure and potentially running first_launch_prompt
settings = load_settings()


# --- NEW FUNCTIONALITY: Check Items Folder and Guide ---
def check_items_folder_and_guide(parent_window):
    """
    Checks if the ITEMS_FOLDER is empty and displays a tutorial if it is.
    """
    folder_is_empty = True
    if os.path.exists(ITEMS_FOLDER):
        if os.listdir(ITEMS_FOLDER): # If listdir returns anything, it's not empty
            folder_is_empty = False

    if folder_is_empty:
        display_items_tutorial(parent_window)

def display_items_tutorial(parent_window):
    """
    Displays a tutorial window instructing the user to dump character .farc files.
    """
    tutorial_win = tk.Toplevel(parent_window)
    tutorial_win.title("Important: Items Folder Setup")
    tutorial_win.geometry("450x230") # Adjusted height for the new message
    tutorial_win.grab_set() # Make it modal
    tutorial_win.resizable(False, False)
    center_window(tutorial_win)

    # FIX: Changed to global function apply_theme_to_window
    apply_theme_to_window(tutorial_win)

    frame = tk.Frame(tutorial_win)
    frame.pack(padx=20, pady=20, fill='both', expand=True)
    theme_manager.apply_theme_to_widget(frame, 'frame')

    # UPDATED MESSAGE
    tk.Label(
        frame,
        text="Hey there! Your 'items' folder is empty. For DivaDivaModule to work properly, you need to put all the character-specific .farc files from your game's archives into this folder. Things like 'cmnitms' or 'hnditms' aren't needed, just the ones for characters. If you try to open an item without these files, it won't work. Hooray!",
        font=('Arial', 10),
        wraplength=400,
        justify='center'
    ).pack(pady=(0, 20))

    def close_tutorial():
        tutorial_win.destroy()

    ok_button = tk.Button(frame, text="Got It!", command=close_tutorial, font=('Arial', 11))
    ok_button.pack(pady=10)
    theme_manager.apply_theme_to_widget(ok_button, 'button')

    tutorial_win.protocol("WM_DELETE_WINDOW", close_tutorial)

    tutorial_win.wait_window(tutorial_win) # Wait for this window to be closed


# --- Rest of the Functions and Classes ---

MODULE_ENTRY_INSTANCES = []

def refresh_all_themes():
    root = tk._default_root
    if root:
        apply_theme_to_window(root, 'default')
        def refresh_window_recursive(window):
            try:
                apply_theme_to_window(window)
                for child in window.winfo_children():
                    if isinstance(child, tk.Toplevel):
                        refresh_window_recursive(child)
            except Exception:
                pass
        all_windows = [root]
        for widget in root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                all_windows.append(widget)
        try:
            for window_name in root.tk.call('winfo', 'children', '.'):
                if window_name != '.':
                    try:
                        window = root.nametowidget(window_name)
                        if isinstance(window, tk.Toplevel) and window not in all_windows:
                            all_windows.append(window)
                    except Exception:
                        pass
        except Exception:
            pass
        for window in all_windows:
            try:
                if window == root:
                    apply_theme_to_window(window, 'default')
                else:
                    apply_theme_to_window(window, 'toplevel')
            except Exception:
                pass
    for entry in MODULE_ENTRY_INSTANCES:
        entry.redraw_theme()

def apply_theme_to_window(window, window_type='toplevel'):
    theme_manager.apply_theme_to_widget(window, window_type)
    def apply_to_children(widget):
        for child in widget.winfo_children():
            try:
                widget_class = child.winfo_class()
                if widget_class == 'Listbox':
                    theme_manager.apply_theme_to_widget(child, 'listbox')
                elif widget_class == 'Entry':
                    theme_manager.apply_theme_to_widget(child, 'entry')
                elif widget_class == 'Button':
                    theme_manager.apply_theme_to_widget(child, 'button')
                elif widget_class == 'Frame':
                    theme_manager.apply_theme_to_widget(child, 'frame')
                elif widget_class == 'Label':
                    theme_manager.apply_theme_to_widget(child, 'label')
                elif widget_class == 'Treeview':
                    theme_manager.apply_theme_to_treeview(child)
                elif widget_class == 'TCombobox':
                    theme_manager.apply_theme_to_combobox(child)
                elif widget_class == 'TSeparator':
                    theme_manager.apply_theme_to_separator(child)
                elif widget_class in ('Radiobutton', 'Checkbutton', 'Scrollbar', 'Menu'):
                    theme_manager.apply_theme_to_widget(child, 'button')
                else:
                    theme_manager.apply_theme_to_widget(child)
                apply_to_children(child)
            except Exception:
                pass
    apply_to_children(window)
    try:
        window.update_idletasks()
    except Exception:
        pass

def load_modules():
    modules = {}
    try:
        with open(MODULES_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                module_id = row.get('Module ID')
                if not module_id:
                    continue
                if module_id not in modules:
                    modules[module_id] = {
                        'Module ID': module_id,
                        'Name (EN)': row.get('Name (EN)', ''),
                        'Name (JP)': row.get('Name (JP)', ''),
                        'Character': row.get('Character', ''),
                        'Source': row.get('Source', ''),
                        'COS ID': row.get('COS ID', ''),
                        'Names': row,
                        'Items': [],
                        '_seen_items': set() # To track unique items for this module
                    }

                current_module = modules[module_id]
                item_data = {
                    'Item ID': row.get('Item ID', ''),
                    'Object(s)': row.get('Object(s)', ''),
                    'Type': row.get('Type', '')
                }

                # Create a tuple from item data to use in the set for uniqueness check
                item_tuple = (item_data['Item ID'], item_data['Object(s)'], item_data['Type'])

                if item_tuple not in current_module['_seen_items']:
                    current_module['Items'].append(item_data)
                    current_module['_seen_items'].add(item_tuple)

        # Clean up the temporary _seen_items set after loading all modules
        for module_data in modules.values():
            if '_seen_items' in module_data:
                del module_data['_seen_items']

    except Exception as e:
        messagebox.showerror("Error", f"{MODULES_CSV} could not be loaded: {e}")
        sys.exit(1) # Use sys.exit for critical errors
    return modules

def open_item_in_mikumikumodel(object_name):
    # Reload settings to ensure we have the latest paths
    current_settings = load_settings()
    mikumikumodel_exe = current_settings.get("mikumikumodel_exe", "")
    wineprefix = current_settings.get("wineprefix", "")

    if not mikumikumodel_exe or not os.path.isfile(mikumikumodel_exe):
        messagebox.showerror("Error", "MikuMikuModel.exe path is not set or invalid in settings. Please configure it in File -> Settings.")
        return

    target = object_name.lower() + ".farc"
    search_dir = ITEMS_FOLDER # Use the ITEMS_FOLDER

    if not os.path.exists(search_dir):
        messagebox.showwarning("Folder Not Found", f"The items folder '{search_dir}' does not exist.")
        return

    item_files = os.listdir(search_dir)
    for fname in item_files:
        if fname.lower() == target:
            filepath = os.path.abspath(os.path.join(search_dir, fname))
            filepath_win = f"Z:{filepath}" # Adjust for Wine path mapping if necessary
            try:
                command = []
                if wineprefix:
                    command.extend(["env", f"WINEPREFIX={wineprefix}"])
                command.extend(["wine", mikumikumodel_exe, filepath_win])
                subprocess.Popen(command)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{filepath}\n\n{e}")
            return
    messagebox.showwarning("File Not Found", f"Item file for '{object_name}' not found in '{search_dir}' folder.")

def save_note(name, module_id, item_id, desc):
    os.makedirs(os.path.dirname(NOTES_CSV), exist_ok=True)
    with open(NOTES_CSV, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, module_id, item_id, desc])

def load_notes():
    notes = {}
    order = []
    if os.path.exists(NOTES_CSV):
        with open(NOTES_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) < 4:
                    continue
                name, module_id, item_id, desc = row
                if name not in notes:
                    notes[name] = []
                    order.append(name)
                notes[name].append((module_id, item_id, desc))
    return notes, order

def save_all_notes(notes):
    os.makedirs(os.path.dirname(NOTES_CSV), exist_ok=True)
    with open(NOTES_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for name, items in notes.items():
            for module_id, item_id, desc in items:
                writer.writerow([name, module_id, item_id, desc])

def open_settings(parent):
    settings_win = tk.Toplevel(parent)
    settings_win.title("Settings")
    settings_win.geometry("500x380") # Increased height to accommodate new fields
    settings_win.resizable(False, False)
    settings_win.grab_set()
    apply_theme_to_window(settings_win)
    center_window(settings_win)

    main_frame = tk.Frame(settings_win, borderwidth=0, relief='flat')
    main_frame.pack(fill='both', expand=True, padx=0, pady=0)
    theme_manager.apply_theme_to_widget(main_frame, 'frame')

    title_label = tk.Label(main_frame, text="Application Settings", font=('Arial', 16, 'bold'))
    title_label.pack(pady=(15, 20))
    theme_manager.apply_theme_to_widget(title_label, 'label')

    current_settings = load_settings() # Load current settings

    # --- MikuMikuModel Path Setting ---
    exe_path_frame = tk.Frame(main_frame)
    exe_path_frame.pack(fill='x', padx=20, pady=5)
    theme_manager.apply_theme_to_widget(exe_path_frame, 'frame')

    tk.Label(exe_path_frame, text="MikuMikuModel.exe Path:", anchor='w').pack(fill='x')
    exe_var = tk.StringVar(value=current_settings.get("mikumikumodel_exe", ""))
    exe_entry = tk.Entry(exe_path_frame, textvariable=exe_var)
    exe_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
    theme_manager.apply_theme_to_widget(exe_entry, 'entry')

    def browse_exe_path():
        path = filedialog.askopenfilename(title="Select MikuMikuModel.exe", filetypes=[("Exe files", "*.exe")])
        if path:
            exe_var.set(path)
    tk.Button(exe_path_frame, text="Browse", command=browse_exe_path).pack(side='right')

    # --- Wine Prefix Path Setting ---
    wine_path_frame = tk.Frame(main_frame)
    wine_path_frame.pack(fill='x', padx=20, pady=5)
    theme_manager.apply_theme_to_widget(wine_path_frame, 'frame')

    tk.Label(wine_path_frame, text="Wine Prefix Path (Optional):", anchor='w').pack(fill='x')
    wine_var = tk.StringVar(value=current_settings.get("wineprefix", ""))
    wine_entry = tk.Entry(wine_path_frame, textvariable=wine_var)
    wine_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
    theme_manager.apply_theme_to_widget(wine_entry, 'entry')

    def browse_wine_path():
        path = filedialog.askdirectory(title="Select Wine Prefix Directory")
        if path:
            wine_var.set(path)
    tk.Button(wine_path_frame, text="Browse", command=browse_wine_path).pack(side='right')

    # --- Separator ---
    ttk.Separator(main_frame, orient='horizontal').pack(fill='x', padx=20, pady=10)

    # --- Theme Settings ---
    theme_frame = tk.Frame(main_frame, borderwidth=0, relief='flat')
    theme_frame.pack(fill='x', padx=20, pady=(0, 10))
    theme_manager.apply_theme_to_widget(theme_frame, 'frame')

    theme_label = tk.Label(theme_frame, text="Theme:", font=('Arial', 12, 'bold'))
    theme_label.pack(anchor='w', pady=(0, 5))
    theme_manager.apply_theme_to_widget(theme_label, 'label')

    theme_var = tk.StringVar(value=theme_manager.current_theme.title())
    def on_theme_change():
        new_theme = theme_var.get().lower()
        if new_theme != theme_manager.current_theme:
            theme_manager.set_theme(new_theme)
            refresh_all_themes() # Refresh main window and popups

    light_radio = tk.Radiobutton(
        theme_frame, text="Light Theme", variable=theme_var, value="Light",
        font=('Arial', 10), command=on_theme_change,
        bg=THEMES[theme_manager.current_theme]['bg'],
        fg=THEMES[theme_manager.current_theme]['fg'],
        selectcolor=THEMES[theme_manager.current_theme]['select_bg'],
        activebackground=THEMES[theme_manager.current_theme]['select_bg'],
        activeforeground=THEMES[theme_manager.current_theme]['select_fg'],
        borderwidth=0
    )
    light_radio.pack(anchor='w', pady=2)
    theme_manager.apply_theme_to_widget(light_radio, 'button')

    dark_radio = tk.Radiobutton(
        theme_frame, text="Dark Theme", variable=theme_var, value="Dark",
        font=('Arial', 10), command=on_theme_change,
        bg=THEMES[theme_manager.current_theme]['bg'],
        fg=THEMES[theme_manager.current_theme]['fg'],
        selectcolor=THEMES[theme_manager.current_theme]['select_bg'],
        activebackground=THEMES[theme_manager.current_theme]['select_bg'],
        activeforeground=THEMES[theme_manager.current_theme]['select_fg'],
        borderwidth=0
    )
    dark_radio.pack(anchor='w', pady=2)
    theme_manager.apply_theme_to_widget(dark_radio, 'button')

    # --- Buttons ---
    button_frame = tk.Frame(main_frame, borderwidth=0, relief='flat')
    button_frame.pack(fill='x', pady=(20, 10))
    theme_manager.apply_theme_to_widget(button_frame, 'frame')

    def save_current_settings():
        updated_settings = {
            "mikumikumodel_exe": exe_var.get().strip(),
            "wineprefix": wine_var.get().strip(),
            "theme": theme_manager.current_theme # Ensure current theme is also saved
        }
        try:
            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(updated_settings, f, indent=4)
            messagebox.showinfo("Settings Saved", "Application settings have been saved.")
            # Reload settings globally in main app if necessary (e.g., if mikumikumodel_exe changed)
            # For this simple setup, reloading `MIKUMIKUMODEL_EXE` and `WINEPREFIX` inside
            # `open_item_in_mikumikumodel` on each call is safer.
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    save_btn = tk.Button(
        button_frame, text="Save Settings", command=save_current_settings,
        font=('Arial', 10), padx=20, borderwidth=0
    )
    save_btn.pack(side='right', padx=(5, 0))
    theme_manager.apply_theme_to_widget(save_btn, 'button')

    def reset_settings():
        theme_manager.set_theme('light')
        theme_var.set('Light') # Update radio button
        refresh_all_themes() # Apply theme change
        exe_var.set("") # Clear MMM path
        wine_var.set("") # Clear Wine prefix
        # Reset other settings in the file
        try:
            current_settings_data = {}
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    current_settings_data = json.load(f)

            current_settings_data['mikumikumodel_exe'] = ""
            current_settings_data['wineprefix'] = ""
            current_settings_data['theme'] = 'light' # Default theme
            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(current_settings_data, f, indent=4)
            messagebox.showinfo("Settings Reset", "Application settings have been reset to default. You may be prompted to set up MikuMikuModel.exe on next launch.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset other settings: {e}")

    reset_btn = tk.Button(
        button_frame, text="Reset to Default", command=reset_settings,
        font=('Arial', 10), padx=20, borderwidth=0
    )
    reset_btn.pack(side='right', padx=(5, 0))
    theme_manager.apply_theme_to_widget(reset_btn, 'button')

    close_btn = tk.Button(
        button_frame, text="Close", command=settings_win.destroy,
        font=('Arial', 10), padx=20, borderwidth=0
    )
    close_btn.pack(side='right', padx=(5, 0))
    theme_manager.apply_theme_to_widget(close_btn, 'button')


class ModuleEntry(tk.Frame):
    _image_cache = {}
    ENTRY_HEIGHT = 28
    GRADIENT_PORTION = 0.55

    def __init__(self, parent, module, select_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.module = module
        self.select_callback = select_callback
        self.selected = False
        self.bg_color, self.gradient_color = self._get_colors()
        self.canvas = tk.Canvas(
            self,
            height=self.ENTRY_HEIGHT,
            highlightthickness=0,
            bd=0,
            bg=theme_manager.get_theme()['bg']
        )
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind("<Button-1>", self._on_select)
        self.bind("<Button-1>", self._on_select)

        img = self._load_character_image()
        self.img_ref = img
        self.mid = module['Module ID']
        self.name = module['Name (EN)']
        self.char = module['Character']
        self.display_name = f"[{self.mid}] {self.name} ({self.char})"
        self.text_id = None
        self.gradient_img = None
        self.last_drawn_width = None
        self.bind('<Configure>', self._on_resize)
        MODULE_ENTRY_INSTANCES.append(self)

    def destroy(self):
        try:
            MODULE_ENTRY_INSTANCES.remove(self)
        except ValueError:
            pass
        super().destroy()

    def is_visible(self):
        try:
            # Need to get the canvas object from the scrollable_frame's parent
            canvas = self.master.master # Assuming self is in scrollable_frame, which is in canvas

            self.update_idletasks() # Ensure widget has current geometry
            canvas.update_idletasks() # Ensure canvas has current scroll position

            # Get widget's position relative to its parent frame (scrollable_frame)
            widget_y_in_frame = self.winfo_y()

            # Get canvas scroll position (fractional)
            y_min_fraction, y_max_fraction = canvas.yview()

            # Calculate total scrollable height in pixels
            scroll_region_height = canvas.bbox("all")[3] if canvas.bbox("all") else canvas.winfo_height()

            # Convert fractional scroll to pixel offset
            scroll_offset_pixels = y_min_fraction * scroll_region_height

            # Calculate widget's absolute position on the canvas
            widget_top_on_canvas = widget_y_in_frame - scroll_offset_pixels
            widget_bottom_on_canvas = widget_top_on_canvas + self.ENTRY_HEIGHT

            # Get visible height of the canvas
            canvas_height = canvas.winfo_height()

            # Check if any part of the widget is within the visible canvas area
            return (widget_bottom_on_canvas > 0 and widget_top_on_canvas < canvas_height)
        except Exception:
            # If there's an error (e.g., widget not yet mapped), assume it needs drawing
            return True


    def _on_resize(self, event):
        self.last_drawn_width = event.width
        # Ensure gradient is drawn on resize
        self._draw_gradient(self.bg_color, self.gradient_color)


    def _draw_gradient(self, color1, color2):
        w = self.winfo_width() or self.master.winfo_width() or 600
        h = self.ENTRY_HEIGHT
        grad_start = int(w * (1 - self.GRADIENT_PORTION))
        grad_end = w

        self.canvas.delete("all")

        self.canvas.create_rectangle(0, 0, grad_start, h, fill=color1, outline="")

        gradient_width = grad_end - grad_start
        if gradient_width < 1:
            gradient_width = 1

        img = Image.new("RGB", (gradient_width, h), color1)
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)
        for x in range(gradient_width):
            ratio = x / (gradient_width - 1) if gradient_width > 1 else 1
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            for y in range(h):
                img.putpixel((x, y), (r, g, b))

        self.gradient_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(grad_start, 0, anchor='nw', image=self.gradient_img)

        if hasattr(self, "img_ref") and self.img_ref:
            self.canvas.create_image(4, 2, image=self.img_ref, anchor='nw')

        text_x = 42
        if self.text_id:
            self.canvas.delete(self.text_id)
        self.text_id = self.canvas.create_text(
            text_x, h // 2, anchor='w',
            text=self.display_name,
            font=('Arial', 10, 'bold'),
            fill="#222" if self._is_light_theme() else "#eee"
        )

    def redraw_theme(self):
        # Update colors based on current theme
        self.bg_color, self.gradient_color = self._get_colors()
        # Only redraw the gradient if the entry is visible
        if self.is_visible():
            self._draw_gradient(self.bg_color, self.gradient_color)


    def _on_select(self, event=None):
        self.select_callback(self.module)

    def _hex_to_rgb(self, hexcolor):
        hexcolor = hexcolor.lstrip('#')
        return tuple(int(hexcolor[i:i+2], 16) for i in (0, 2, 4))

    def _load_character_image(self):
        char = self.module['Character']
        fname = f"{char}.png"
        fpath = os.path.join(IMAGES_FOLDER, fname)
        if not os.path.isfile(fpath):
            fname = f"{char.lower().replace(' ', '_')}.png"
            fpath = os.path.join(IMAGES_FOLDER, fname)
        if not os.path.isfile(fpath):
            return None
        if fpath not in ModuleEntry._image_cache:
            pil_img = Image.open(fpath).convert("RGBA")
            pil_img = pil_img.resize((24, 24), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(pil_img)
            ModuleEntry._image_cache[fpath] = img
        return ModuleEntry._image_cache[fpath]

    def _get_colors(self):
        char = self.module['Character']
        color = CHARACTER_COLORS.get(char, "#DDDDDD")
        theme_bg = theme_manager.get_theme()['bg']
        return (theme_bg, color)

    def _is_light_theme(self):
        return theme_manager.current_theme == "light"

# Global variables used in populate_module_entries and related functions
modules = {}
module_keys = []
canvas = None
scrollable_frame = None
search_var = None
filter_var = None
_redraw_visible_entries_on_canvas = None # Defined later in main()
show_module_details = None # Defined later in main()


def populate_module_entries():
    filtered_modules = []
    search_term = search_var.get().lower()
    char_filter = filter_var.get()
    for mid in module_keys:
        module = modules[mid]
        if char_filter != "All Characters" and module['Character'] != char_filter:
            continue
        display_name = f"[{mid}] {module['Name (EN)']} ({module['Character']})"
        if search_term in display_name.lower():
            filtered_modules.append(module)

    for entry in list(MODULE_ENTRY_INSTANCES): # Iterate over a copy
        entry.destroy()

    MODULE_ENTRY_INSTANCES.clear() # Ensure the global list is fully cleared

    for module in filtered_modules:
        entry = ModuleEntry(
            scrollable_frame, module,
            select_callback=show_module_details
        )
        entry.pack(fill='x', pady=1)

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    _redraw_visible_entries_on_canvas()


def main():
    global modules, module_keys, canvas, scrollable_frame, search_var, filter_var, _redraw_visible_entries_on_canvas, show_module_details

    ensure_app_structure() # Ensure app structure is set up first
    settings = load_settings() # Load settings after ensuring the app structure and potentially running first_launch_prompt

    modules = load_modules()
    module_keys = list(modules.keys())

    root = tk.Tk()
    root.title("DivaDivaModule")
    root.geometry("900x700")
    apply_theme_to_window(root, 'default')
    center_window(root)

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open Settings", command=lambda: open_settings(root))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    search_filter_frame = tk.Frame(root, pady=10)
    search_filter_frame.pack(fill='x', padx=10)
    theme_manager.apply_theme_to_widget(search_filter_frame, 'frame')

    search_label = tk.Label(search_filter_frame, text="Search Module:")
    search_label.pack(side='left', padx=(0, 5))
    theme_manager.apply_theme_to_widget(search_label, 'label')

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_filter_frame, textvariable=search_var)
    search_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
    theme_manager.apply_theme_to_widget(search_entry, 'entry')

    char_options = ["All Characters"] + sorted(list(CHARACTER_COLORS.keys()))
    filter_var = tk.StringVar(value="All Characters")
    filter_menu = ttk.Combobox(search_filter_frame, textvariable=filter_var, values=char_options, state='readonly', width=20)
    filter_menu.pack(side='left')
    theme_manager.apply_theme_to_combobox(filter_menu)

    main_content_frame = tk.Frame(root)
    main_content_frame.pack(fill='both', expand=True, padx=10, pady=10)
    theme_manager.apply_theme_to_widget(main_content_frame, 'frame')

    module_list_frame = tk.Frame(main_content_frame)
    module_list_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
    theme_manager.apply_theme_to_widget(module_list_frame, 'frame')

    canvas = tk.Canvas(module_list_frame, highlightthickness=0, bd=0)
    canvas.pack(side='left', fill='both', expand=True)
    theme_manager.apply_theme_to_widget(canvas)

    scrollbar = ttk.Scrollbar(module_list_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas)
    theme_manager.apply_theme_to_widget(scrollable_frame, 'frame')
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw', tags="scrollable_frame_tag")

    def _on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", _on_frame_configure)

    def _redraw_visible_entries_on_canvas_func(): # Renamed to avoid global conflict
        canvas_y_offset = canvas.canvasy(0)
        canvas_height = canvas.winfo_height()

        for entry in MODULE_ENTRY_INSTANCES:
            try:
                # Ensure entry is still mapped and visible on screen
                if not entry.winfo_exists():
                    continue

                entry_y_in_frame = entry.winfo_y()
                entry_top_on_canvas = entry_y_in_frame - canvas_y_offset
                entry_bottom_on_canvas = entry_top_on_canvas + ModuleEntry.ENTRY_HEIGHT

                # Check if any part of the widget is within the visible canvas area
                if entry_bottom_on_canvas > 0 and entry_top_on_canvas < canvas_height:
                    entry.redraw_theme() # Call redraw_theme to ensure it draws correctly
                else:
                    # Optionally, clear entries that are far off-screen to save resources
                    # For now, we just don't redraw them.
                    pass
            except tk.TclError:
                # Widget might have been destroyed in the interim
                pass

    _redraw_visible_entries_on_canvas = _redraw_visible_entries_on_canvas_func # Assign to global

    canvas.bind("<Configure>", lambda event: _redraw_visible_entries_on_canvas())
    canvas.bind("<MouseWheel>", lambda event: (canvas.yview_scroll(int(-1*(event.delta/120)), "units"), _redraw_visible_entries_on_canvas()))
    canvas.bind("<Button-4>", lambda event: (canvas.yview_scroll(-1, "units"), _redraw_visible_entries_on_canvas()))
    canvas.bind("<Button-5>", lambda event: (canvas.yview_scroll(1, "units"), _redraw_visible_entries_on_canvas()))

    module_details_frame = tk.Frame(main_content_frame, width=400)
    module_details_frame.pack(side='right', fill='y')
    module_details_frame.pack_propagate(0)
    theme_manager.apply_theme_to_widget(module_details_frame, 'frame')

    separator = ttk.Separator(main_content_frame, orient='vertical')
    separator.pack(side='right', fill='y', padx=(5, 5))
    theme_manager.apply_theme_to_separator(separator)

    details_labels = {}
    label_font = ('Arial', 10)
    for i, (key_en, key_jp) in enumerate([
        ("Module ID", "モジュールID"),
        ("Name (EN)", "英語名"),
        ("Name (JP)", "日本語名"),
        ("Character", "キャラクター"),
        ("Source", "出典"),
        ("COS ID", "コスID")
    ]):
        row_frame = tk.Frame(module_details_frame)
        row_frame.pack(fill='x', pady=1, padx=5)
        theme_manager.apply_theme_to_widget(row_frame, 'frame')

        label_en = tk.Label(row_frame, text=f"{key_en}:", font=label_font, anchor='w', width=10)
        label_en.pack(side='left')
        theme_manager.apply_theme_to_widget(label_en, 'label')

        value_label = tk.Label(row_frame, text="", font=label_font, anchor='w', wraplength=250, justify='left')
        value_label.pack(side='left', fill='x', expand=True)
        theme_manager.apply_theme_to_widget(value_label, 'label')

        details_labels[key_en] = value_label

    tk.Label(module_details_frame, text="Items:", font=('Arial', 10, 'bold'), anchor='w').pack(fill='x', pady=(5,0), padx=5)

    item_tree = ttk.Treeview(module_details_frame, columns=("Item ID", "Object(s)", "Type"), show='headings')
    item_tree.heading("Item ID", text="Item ID")
    item_tree.heading("Object(s)", text="Object(s)")
    item_tree.heading("Type", text="Type")
    item_tree.column("Item ID", width=80, stretch=tk.NO)
    item_tree.column("Object(s)", width=150)
    item_tree.column("Type", width=80, stretch=tk.NO)
    item_tree.pack(fill='both', expand=True, padx=5)
    theme_manager.apply_theme_to_treeview(item_tree)

    def show_module_details_func(module): # Renamed to avoid global conflict
        for key, label_widget in details_labels.items():
            label_widget.config(text=module.get(key, ''))

        for i in item_tree.get_children():
            item_tree.delete(i)

        for item in module.get('Items', []):
            item_tree.insert('', 'end', values=(
                item.get('Item ID', ''),
                item.get('Object(s)', ''),
                item.get('Type', '')
            ))

        item_tree_context_menu = tk.Menu(root, tearoff=0)
        item_tree_context_menu.add_command(label="Open Item in MikuMikuModel", command=lambda: on_item_double_click(None))

        def show_item_context_menu(event):
            item_tree.identify_row(event.y)
            item_tree.selection_set(item_tree.identify_row(event.y))
            item_tree_context_menu.post(event.x_root, event.y_root)

        item_tree.bind("<Button-3>", show_item_context_menu)

    show_module_details = show_module_details_func # Assign to global

    def on_item_double_click(event):
        selected = item_tree.selection()
        if selected:
            values = item_tree.item(selected[0], 'values')
            object_name = values[1]
            open_item_in_mikumikumodel(object_name)

    item_tree.bind("<Double-1>", on_item_double_click)

    search_var.trace_add("write", lambda *_: populate_module_entries())
    filter_menu.bind("<<ComboboxSelected>>", lambda e: populate_module_entries())
    populate_module_entries()

    notes_btn = tk.Button(root, text="FrankenNotes", command=lambda: open_notes_view(modules))
    notes_btn.pack(pady=5)
    theme_manager.apply_theme_to_widget(notes_btn, 'button')

    theme_manager.load_settings()
    refresh_all_themes()

    # --- Call check_items_folder_and_guide AFTER the main window is set up but before mainloop ---
    # This ensures the main window is visible when the tutorial pops up.
    check_items_folder_and_guide(root)

    root.mainloop()

if __name__ == "__main__":
    main()
