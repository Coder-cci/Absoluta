import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import hashlib
import os
import secrets
import re
import random


class RetroColors:
    BG_GRAY = "#c0c0c0"
    BG_LIGHT = "#d4d0c8"
    BG_DARK = "#808080"
    WINDOW_BG = "#c0c0c0"
    BUTTON_FACE = "#c0c0c0"
    BUTTON_HIGHLIGHT = "#ffffff"
    BUTTON_SHADOW = "#808080"
    TEXT_BG = "#ffffff"
    TEXT_FG = "#000000"
    SELECTED = "#000080"
    SELECTED_TEXT = "#ffffff"
    DISABLED = "#808080"
    BORDER = "#000000"
    ERROR = "#ff0000"


class RetroFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=RetroColors.BG_GRAY, **kwargs)
        self.configure(relief=tk.RAISED, bd=2)


class RetroLabelFrame(tk.LabelFrame):
    def __init__(self, parent, text="", **kwargs):
        super().__init__(parent, text=text, bg=RetroColors.BG_GRAY, fg=RetroColors.TEXT_FG,
                         relief=tk.RIDGE, bd=2, font=("MS Sans Serif", 9, "bold"), **kwargs)


class RetroButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=RetroColors.BUTTON_FACE, fg=RetroColors.TEXT_FG,
                         relief=tk.RAISED, bd=2, font=("MS Sans Serif", 9),
                         activebackground=RetroColors.BUTTON_FACE,
                         activeforeground=RetroColors.TEXT_FG,
                         highlightbackground=RetroColors.BG_GRAY,
                         highlightthickness=0, **kwargs)


class RetroEntry(tk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=RetroColors.TEXT_BG, fg=RetroColors.TEXT_FG,
                         relief=tk.SUNKEN, bd=2, font=("Fixedsys", 10), **kwargs)


class RetroCombobox(ttk.Combobox):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(font=("MS Sans Serif", 9))


class RetroRadiobutton(tk.Radiobutton):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=RetroColors.BG_GRAY, fg=RetroColors.TEXT_FG,
                         activebackground=RetroColors.BG_GRAY,
                         activeforeground=RetroColors.TEXT_FG,
                         highlightbackground=RetroColors.BG_GRAY,
                         font=("MS Sans Serif", 9), **kwargs)


class RetroScrolledText(scrolledtext.ScrolledText):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=RetroColors.TEXT_BG, fg=RetroColors.TEXT_FG,
                         relief=tk.SUNKEN, bd=2, font=("Fixedsys", 10),
                         insertbackground=RetroColors.TEXT_FG,
                         highlightbackground=RetroColors.BG_GRAY,
                         highlightthickness=2, **kwargs)


class SourceAlphabet:
    ASCII = "".join(chr(i) for i in range(32, 127))
    RUSSIAN = "".join(
        chr(i) for i in range(32, 127)) + "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    MATH = "".join(chr(i) for i in range(32,
                                         127)) + "∀∁∂∃∄∅∆∇∈∉∊∋∌∍∎∏∐∑−∓∔∕∖∗∘∙√∛∜∝∞∟∠∡∢∣∤∥∦∧∨∩∪∫∬∭∮∯∰∱∲∳∴∵∶∷∸∹∺∻∼∽∾∿≀≁≂≃≄≅≆≇≈≉≊≋≌≍≎≏≐≑≒≓≔≕≖≗≘≙≚≛≜≝≞≟≠≡≢≣≤≥≦≧≨≩≪≫≬≭≮≯≰≱≲≳≴≵≶≷≸≹≺≻≼≽≾≿⊀⊁⊂⊃⊄⊅⊆⊇⊈⊉⊊⊋⊌⊍⊎⊏⊐⊑⊒⊓⊔⊕⊖⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊱⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⋀⋁⋂⋃⋄⋅⋆⋇⋈⋉⋊⋋⋌⋍⋎⋏⋐⋑⋒⋓⋔⋕⋖⋗⋘⋙⋚⋛⋜⋝⋞⋟⋠⋡⋢⋣⋤⋥⋦⋧⋨⋩⋪⋫⋬⋭⋮⋯⋰⋱⋲⋳⋴⋵⋶⋷⋸⋹⋺⋻⋼⋽⋾⋿"

    ALPHABETS = {
        "ASCII (English + digits + symbols)": ASCII,
        "Russian + ASCII": RUSSIAN,
        "Mathematical symbols": MATH,
    }

    @classmethod
    def get_names(cls):
        return list(cls.ALPHABETS.keys())

    @classmethod
    def get(cls, name):
        return cls.ALPHABETS.get(name, cls.ASCII)


class CipherAlphabet:
    def __init__(self, filename):
        self.filename = filename
        self.symbols = []
        self.visual_chars = []
        self.load()

    def load(self):
        try:
            with open(self.filename, 'r', encoding='utf-8-sig') as f:
                content = f.read()
                self.visual_chars = list(content)
                self.symbols = list(content)

            print(f"Loaded cipher alphabet: {self.filename}")
            print(f"  Visual characters: {len(self.visual_chars)}")
            print(f"  Code positions: {len(self.symbols)}")

        except FileNotFoundError:
            print(f"File {self.filename} not found!")
            self.symbols = [chr(i) for i in range(65, 91)]
            self.visual_chars = self.symbols.copy()
        except Exception as e:
            print(f"Load error: {e}")
            self.symbols = []
            self.visual_chars = []

    def __len__(self):
        return len(self.symbols)

    def get_symbol(self, index):
        if 0 <= index < len(self.symbols):
            return self.symbols[index]
        return '?'

    def get_index(self, symbol):
        try:
            return self.symbols.index(symbol)
        except ValueError:
            return -1


class CSPRNG:
    def __init__(self, seed_hex):
        self.seed = seed_hex.encode('utf-8')
        self.counter = 0
        self.buffer = b''
        self.buffer_pos = 0

    def _refill_buffer(self):
        data = self.seed + str(self.counter).encode('utf-8')
        self.buffer = hashlib.sha256(data).digest()
        self.counter += 1
        self.buffer_pos = 0

    def get_byte(self):
        if self.buffer_pos >= len(self.buffer):
            self._refill_buffer()
        byte = self.buffer[self.buffer_pos]
        self.buffer_pos += 1
        return byte

    def get_int(self, max_val):
        if max_val <= 0:
            return 0

        if max_val <= 256:
            while True:
                b = self.get_byte()
                if b < max_val:
                    return b
        elif max_val <= 65536:
            while True:
                b1 = self.get_byte()
                b2 = self.get_byte()
                val = (b1 << 8) | b2
                if val < max_val:
                    return val
        else:
            while True:
                b1 = self.get_byte()
                b2 = self.get_byte()
                b3 = self.get_byte()
                val = (b1 << 16) | (b2 << 8) | b3
                if val < max_val:
                    return val


class RetroCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Absoluta")
        self.root.geometry("900x800")
        self.root.configure(bg=RetroColors.BG_GRAY)

        self.root.resizable(False, False)

        self.alphabet_folder = os.path.join(os.path.dirname(__file__), "alphabets")
        
        if not os.path.exists(self.alphabet_folder):
            os.makedirs(self.alphabet_folder)
            print(f"Created alphabets folder: {self.alphabet_folder}")

        self.current_cipher_alphabet = None

        self.setup_ui()

        self.generate_random_params()

        self.refresh_alphabet_list()
        self.load_cipher_alphabet()
        self.update_key_display()

        self.seed_entry.bind('<KeyRelease>', self.on_param_change)
        self.salt_prob_entry.bind('<KeyRelease>', self.on_param_change)
        self.weight_left.bind('<KeyRelease>', self.on_param_change)
        self.weight_mid.bind('<KeyRelease>', self.on_param_change)
        self.weight_right.bind('<KeyRelease>', self.on_param_change)
        self.cipher_alphabet_combo.bind('<<ComboboxSelected>>', self.on_cipher_alphabet_change)
    
    def generate_random_params(self):
        seed = secrets.token_hex(16).upper()
        self.seed_entry.delete(0, tk.END)
        self.seed_entry.insert(0, seed)

        salt_prob = str(random.randint(0, 999)).zfill(3)
        self.salt_prob_entry.delete(0, tk.END)
        self.salt_prob_entry.insert(0, salt_prob)

        weights = ''.join([str(random.randint(0, 3)) for _ in range(3)])
        self.weight_left.delete(0, tk.END)
        self.weight_left.insert(0, weights[0])
        self.weight_mid.delete(0, tk.END)
        self.weight_mid.insert(0, weights[1])
        self.weight_right.delete(0, tk.END)
        self.weight_right.insert(0, weights[2])
    
    def setup_ui(self):
        menubar = tk.Menu(self.root, bg=RetroColors.BG_GRAY, fg=RetroColors.TEXT_FG,
                          relief=tk.RAISED, bd=2)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0, bg=RetroColors.BG_GRAY, fg=RetroColors.TEXT_FG,
                            relief=tk.RAISED, bd=2)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load file", command=self.load_file)
        file_menu.add_command(label="Save file", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0, bg=RetroColors.BG_GRAY, fg=RetroColors.TEXT_FG,
                            relief=tk.RAISED, bd=2)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear", command=self.clear_all)
        edit_menu.add_command(label="Generate seed", command=self.generate_seed)

        help_menu = tk.Menu(menubar, tearoff=0, bg=RetroColors.BG_GRAY, fg=RetroColors.TEXT_FG,
                            relief=tk.RAISED, bd=2)
        menubar.add_cascade(label="?", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        main_frame = tk.Frame(self.root, bg=RetroColors.BG_GRAY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        key_frame = RetroLabelFrame(main_frame, text=" Key parameters ")
        key_frame.pack(fill=tk.X, pady=2)

        seed_frame = tk.Frame(key_frame, bg=RetroColors.BG_GRAY)
        seed_frame.pack(fill=tk.X, pady=2, padx=5)

        tk.Label(seed_frame, text="Seed (32 chars):", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=2)
        self.seed_entry = RetroEntry(seed_frame, width=45)
        self.seed_entry.pack(side=tk.LEFT, padx=2)
        self.seed_entry.insert(0, "7F3A9C2B1D8E4F6A5C3B2A1D9E8F7C6B")

        self.gen_seed_btn = RetroButton(seed_frame, text="Generate", command=self.generate_seed)
        self.gen_seed_btn.pack(side=tk.LEFT, padx=5)

        salt_frame = tk.Frame(key_frame, bg=RetroColors.BG_GRAY)
        salt_frame.pack(fill=tk.X, pady=2, padx=5)

        tk.Label(salt_frame, text="Salt probability (000-999):", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=2)
        self.salt_prob_entry = RetroEntry(salt_frame, width=10)
        self.salt_prob_entry.pack(side=tk.LEFT, padx=2)
        self.salt_prob_entry.insert(0, "075")

        self.salt_percent_label = tk.Label(salt_frame, text="→ 7.5%", bg=RetroColors.BG_GRAY,
                                           font=("MS Sans Serif", 9))
        self.salt_percent_label.pack(side=tk.LEFT, padx=5)

        weights_frame = tk.Frame(key_frame, bg=RetroColors.BG_GRAY)
        weights_frame.pack(fill=tk.X, pady=2, padx=5)

        tk.Label(weights_frame, text="Position weights (0-3):", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=2)

        tk.Label(weights_frame, text="left", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=2)
        self.weight_left = RetroEntry(weights_frame, width=3)
        self.weight_left.pack(side=tk.LEFT, padx=2)
        self.weight_left.insert(0, "1")

        tk.Label(weights_frame, text="middle", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=2)
        self.weight_mid = RetroEntry(weights_frame, width=3)
        self.weight_mid.pack(side=tk.LEFT, padx=2)
        self.weight_mid.insert(0, "2")

        tk.Label(weights_frame, text="right", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=2)
        self.weight_right = RetroEntry(weights_frame, width=3)
        self.weight_right.pack(side=tk.LEFT, padx=2)
        self.weight_right.insert(0, "3")

        tk.Label(weights_frame, text="(0=0%, 1=33%, 2=66%, 3=99%)", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 8)).pack(side=tk.LEFT, padx=5)

        cipher_frame = tk.Frame(key_frame, bg=RetroColors.BG_GRAY)
        cipher_frame.pack(fill=tk.X, pady=2, padx=5)

        tk.Label(cipher_frame, text="Cipher alphabet:", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=2)
        
        self.cipher_alphabet_combo = RetroCombobox(cipher_frame, values=[], width=35)
        self.cipher_alphabet_combo.pack(side=tk.LEFT, padx=2)
        self.cipher_alphabet_combo.bind('<<ComboboxSelected>>', self.on_cipher_alphabet_change)

        self.cipher_alphabet_info = tk.Label(cipher_frame, text="", bg=RetroColors.BG_GRAY,
                                             font=("MS Sans Serif", 9))
        self.cipher_alphabet_info.pack(side=tk.LEFT, padx=5)

        key_display_frame = tk.Frame(key_frame, bg=RetroColors.BG_GRAY)
        key_display_frame.pack(fill=tk.X, pady=5, padx=5)

        tk.Label(key_display_frame, text="Final key:", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=2)
        self.key_display = RetroEntry(key_display_frame, width=70)
        self.key_display.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        text_frame = RetroLabelFrame(main_frame, text=" Text ")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=2)

        source_frame = tk.Frame(text_frame, bg=RetroColors.BG_GRAY)
        source_frame.pack(fill=tk.X, pady=2, padx=5)

        tk.Label(source_frame, text="Source alphabet:", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=2)
        self.source_alphabet_combo = RetroCombobox(source_frame, values=SourceAlphabet.get_names(), width=30)
        self.source_alphabet_combo.pack(side=tk.LEFT, padx=2)
        self.source_alphabet_combo.current(0)
        self.source_alphabet_combo.bind('<<ComboboxSelected>>', self.update_source_alphabet_info)

        self.source_alphabet_info = tk.Label(source_frame, text="", bg=RetroColors.BG_GRAY,
                                             font=("MS Sans Serif", 9))
        self.source_alphabet_info.pack(side=tk.LEFT, padx=5)
        self.update_source_alphabet_info()

        input_label = tk.Label(text_frame, text="Input:", bg=RetroColors.BG_GRAY,
                               font=("MS Sans Serif", 9), anchor=tk.W)
        input_label.pack(fill=tk.X, padx=5, pady=(2, 0))

        self.input_text = RetroScrolledText(text_frame, height=6)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        self.input_text.insert(tk.END, "Hello, world! This is a test message.")

        result_frame = RetroLabelFrame(main_frame, text=" Result ")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=2)

        stats_frame = tk.Frame(result_frame, bg=RetroColors.BG_GRAY, relief=tk.SUNKEN, bd=2)
        stats_frame.pack(fill=tk.X, pady=2, padx=5)

        stats_inner = tk.Frame(stats_frame, bg=RetroColors.BG_GRAY)
        stats_inner.pack(pady=2, padx=5)

        tk.Label(stats_inner, text="Input length:", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=2)
        self.src_len_label = tk.Label(stats_inner, text="0", bg=RetroColors.BG_GRAY,
                                      font=("MS Sans Serif", 9, "bold"))
        self.src_len_label.pack(side=tk.LEFT, padx=5)

        tk.Label(stats_inner, text="|", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=5)

        tk.Label(stats_inner, text="Result length:", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=2)
        self.res_len_label = tk.Label(stats_inner, text="0", bg=RetroColors.BG_GRAY,
                                      font=("MS Sans Serif", 9, "bold"))
        self.res_len_label.pack(side=tk.LEFT, padx=5)

        tk.Label(stats_inner, text="|", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=5)

        tk.Label(stats_inner, text="Alphabet:", bg=RetroColors.BG_GRAY,
                 font=("MS Sans Serif", 9)).pack(side=tk.LEFT, padx=2)
        self.cipher_size_label = tk.Label(stats_inner, text="", bg=RetroColors.BG_GRAY,
                                          font=("MS Sans Serif", 9, "bold"))
        self.cipher_size_label.pack(side=tk.LEFT, padx=5)

        output_label = tk.Label(result_frame, text="Output:", bg=RetroColors.BG_GRAY,
                                font=("MS Sans Serif", 9), anchor=tk.W)
        output_label.pack(fill=tk.X, padx=5, pady=(2, 0))

        self.output_text = RetroScrolledText(result_frame, height=6)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        control_frame = tk.Frame(main_frame, bg=RetroColors.BG_GRAY)
        control_frame.pack(fill=tk.X, pady=5)

        mode_frame = tk.Frame(control_frame, bg=RetroColors.BG_GRAY, relief=tk.SUNKEN, bd=2)
        mode_frame.pack(side=tk.LEFT, padx=2)

        self.mode_var = tk.StringVar(value="encrypt")

        encrypt_radio = RetroRadiobutton(mode_frame, text="Encrypt", variable=self.mode_var, value="encrypt")
        encrypt_radio.pack(side=tk.LEFT, padx=5, pady=2)

        decrypt_radio = RetroRadiobutton(mode_frame, text="Decrypt", variable=self.mode_var, value="decrypt")
        decrypt_radio.pack(side=tk.LEFT, padx=5, pady=2)

        RetroButton(control_frame, text="Execute", command=self.run, width=12).pack(side=tk.LEFT, padx=2)
        RetroButton(control_frame, text="Clear", command=self.clear_all, width=10).pack(side=tk.LEFT, padx=2)
        RetroButton(control_frame, text="Load", command=self.load_file, width=10).pack(side=tk.LEFT, padx=2)
        RetroButton(control_frame, text="Save", command=self.save_file, width=10).pack(side=tk.LEFT, padx=2)

        status_frame = tk.Frame(main_frame, bg=RetroColors.BG_GRAY, relief=tk.SUNKEN, bd=2)
        status_frame.pack(fill=tk.X, pady=2)

        self.status = tk.Label(status_frame, text="Ready", bg=RetroColors.BG_GRAY,
                               font=("MS Sans Serif", 9), anchor=tk.W)
        self.status.pack(fill=tk.X, padx=2)

    def refresh_alphabet_list(self):
        try:
            if not os.path.exists(self.alphabet_folder):
                os.makedirs(self.alphabet_folder)
                return

            files = [f for f in os.listdir(self.alphabet_folder) if f.endswith('.txt')]
            files.sort()
            
            if not files:
                return
            
            nice_names = []
            for f in files:
                full_path = os.path.join(self.alphabet_folder, f)
                try:
                    with open(full_path, 'r', encoding='utf-8-sig') as file:
                        content = file.read()
                        real_count = len(content)
                    nice_names.append(f"{f} ({real_count} chars)")
                except Exception as e:
                    print(f"Error reading {f}: {e}")
                    nice_names.append(f)
            
            self.cipher_alphabet_combo['values'] = nice_names
            
            if nice_names:
                current = self.cipher_alphabet_combo.get()
                if current not in nice_names:
                    self.cipher_alphabet_combo.current(0)
            
        except Exception as e:
            print(f"Refresh error: {e}")

    def load_cipher_alphabet(self):
        selected = self.cipher_alphabet_combo.get()
        
        if not selected:
            print("No alphabet selected")
            return
        
        if ' ' in selected:
            filename = selected.split(' ')[0]
        else:
            filename = selected
        
        if filename:
            full_path = os.path.join(self.alphabet_folder, filename)
            
            self.current_cipher_alphabet = CipherAlphabet(full_path)
            size = len(self.current_cipher_alphabet)
            info = f"{size} characters"
            self.cipher_alphabet_info.config(text=info)
            self.cipher_size_label.config(text=str(size))
            self.status.config(text=f"Loaded alphabet: {filename} ({info})")

    def on_cipher_alphabet_change(self, event=None):
        self.load_cipher_alphabet()
        self.update_key_display()

    def update_source_alphabet_info(self, event=None):
        name = self.source_alphabet_combo.get()
        alphabet = SourceAlphabet.get(name)
        self.source_alphabet_info.config(text=f"{len(alphabet)} characters")

    def generate_seed(self):
        seed = secrets.token_hex(16).upper()
        self.seed_entry.delete(0, tk.END)
        self.seed_entry.insert(0, seed)
        self.update_key_display()
        self.status.config(text="New seed generated")

    def on_param_change(self, event=None):
        self.update_salt_percent()
        self.update_key_display()

    def update_salt_percent(self):
        try:
            prob = self.salt_prob_entry.get().strip()
            if prob and prob.isdigit() and len(prob) <= 3:
                val = int(prob)
                if 0 <= val <= 999:
                    percent = val / 10
                    self.salt_percent_label.config(text=f"→ {percent}%", fg=RetroColors.TEXT_FG)
                else:
                    self.salt_percent_label.config(text="→ error", fg=RetroColors.ERROR)
            else:
                self.salt_percent_label.config(text="→ error", fg=RetroColors.ERROR)
        except:
            self.salt_percent_label.config(text="→ error", fg=RetroColors.ERROR)

    def validate_params(self):
        try:
            seed = self.seed_entry.get().strip()
            if not seed or len(seed) != 32 or not all(c in '0123456789ABCDEFabcdef' for c in seed):
                return False, "Seed must be 32 hexadecimal characters (0-9, A-F)"

            prob = self.salt_prob_entry.get().strip()
            if not prob or not prob.isdigit() or len(prob) > 3:
                return False, "Salt probability must be a number from 000 to 999"
            prob_val = int(prob)
            if prob_val < 0 or prob_val > 999:
                return False, "Salt probability must be from 000 to 999"

            for name, entry in [("left", self.weight_left), ("middle", self.weight_mid), ("right", self.weight_right)]:
                val = entry.get().strip()
                if not val or not val.isdigit() or len(val) != 1:
                    return False, f"Weight for '{name}' position must be a single digit (0-3)"
                val_int = int(val)
                if val_int < 0 or val_int > 3:
                    return False, f"Weight for '{name}' position must be from 0 to 3"

            return True, "OK"
        except Exception as e:
            return False, str(e)

    def update_key_display(self):
        valid, msg = self.validate_params()
        if not valid:
            self.key_display.delete(0, tk.END)
            self.key_display.insert(0, "PARAMETER ERROR")
            self.key_display.config(fg=RetroColors.ERROR)
            return

        self.key_display.config(fg=RetroColors.TEXT_FG)

        seed = self.seed_entry.get()[:32].ljust(32, '0')
        salt_prob = self.salt_prob_entry.get().zfill(3)[:3]
        weights = (self.weight_left.get() + self.weight_mid.get() + self.weight_right.get())[:3]

        filename = self.cipher_alphabet_combo.get()
        numbers = re.findall(r'\d+', filename)
        alphabet_number = numbers[0] if numbers else "0"

        key = f"{seed}-{salt_prob}-{weights}-{alphabet_number}"
        self.key_display.delete(0, tk.END)
        self.key_display.insert(0, key)

    def parse_key(self, key_string):
        try:
            parts = key_string.split('-')
            if len(parts) != 4:
                raise ValueError("Invalid key format")
            seed, salt_prob, weights, alphabet_number = parts
            return {
                'seed': seed,
                'salt_prob': int(salt_prob) / 1000,
                'weights': [int(w) for w in weights],
                'alphabet_number': alphabet_number
            }
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse key: {e}")
            return None

    def choose_salt_position(self, rng, weights):
        prob = [0, 33, 66, 99]
        probs = [prob[w] for w in weights]

        while True:
            for i in range(3):
                if rng.get_int(100) < probs[i]:
                    return i

    def generate_mask(self, seed, length):
        rng = CSPRNG(seed + "_MASK")
        mask = []
        for _ in range(length):
            mask.append(rng.get_int(len(self.current_cipher_alphabet)))
        return mask

    def run(self):
        valid, msg = self.validate_params()
        if not valid:
            messagebox.showerror("Parameter error", msg)
            return

        if self.mode_var.get() == "encrypt":
            self.encrypt()
        else:
            self.decrypt()

    def encrypt(self):
        if not self.current_cipher_alphabet:
            messagebox.showerror("Error", "Cipher alphabet not loaded")
            return

        source_alphabet_name = self.source_alphabet_combo.get()
        source_alphabet = SourceAlphabet.get(source_alphabet_name)

        key_str = self.key_display.get()
        key_params = self.parse_key(key_str)
        if not key_params:
            return

        rng = CSPRNG(key_params['seed'])

        text = self.input_text.get(1.0, tk.END).rstrip('\n')
        if not text:
            messagebox.showwarning("Warning", "No text to encrypt")
            return

        for char in text:
            if char not in source_alphabet:
                messagebox.showerror("Error",
                                     f"Character '{char}' not in source alphabet!")
                return

        ciphertext = []
        cipher_size = len(self.current_cipher_alphabet)

        for char in text:
            char_index = source_alphabet.index(char)
            x = char_index
            y = rng.get_int(cipher_size)
            has_salt = rng.get_int(1000) < (key_params['salt_prob'] * 1000)

            if has_salt:
                salt_pos = self.choose_salt_position(rng, key_params['weights'])
                salt = rng.get_int(cipher_size)

                if salt_pos == 0:
                    triplet = [salt, x, y]
                elif salt_pos == 1:
                    triplet = [x, salt, y]
                else:
                    triplet = [x, y, salt]

                chars = [self.current_cipher_alphabet.get_symbol(idx) for idx in triplet]
                ciphertext.extend(chars)
            else:
                chars = [self.current_cipher_alphabet.get_symbol(x),
                         self.current_cipher_alphabet.get_symbol(y)]
                ciphertext.extend(chars)

        intermediate = ''.join(ciphertext)

        mask = self.generate_mask(key_params['seed'], len(intermediate))

        final_chars = []
        for i, char in enumerate(intermediate):
            idx = self.current_cipher_alphabet.get_index(char)
            if idx != -1:
                new_idx = idx ^ mask[i]
                final_chars.append(self.current_cipher_alphabet.get_symbol(new_idx))
            else:
                final_chars.append(char)

        result = ''.join(final_chars)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, result)

        self.src_len_label.config(text=str(len(text)))
        self.res_len_label.config(text=str(len(result)))
        self.status.config(text=f"Encrypted {len(text)} → {len(result)} characters (with XOR)")

    def decrypt(self):
        if not self.current_cipher_alphabet:
            messagebox.showerror("Error", "Cipher alphabet not loaded")
            return

        source_alphabet_name = self.source_alphabet_combo.get()
        source_alphabet = SourceAlphabet.get(source_alphabet_name)

        key_str = self.key_display.get()
        key_params = self.parse_key(key_str)
        if not key_params:
            return

        ciphertext = self.input_text.get(1.0, tk.END).rstrip('\n')
        if not ciphertext:
            messagebox.showwarning("Warning", "No text to decrypt")
            return

        chars = list(ciphertext)
        total_chars = len(chars)

        mask = self.generate_mask(key_params['seed'], total_chars)

        unmasked_chars = []
        for i, char in enumerate(chars):
            idx = self.current_cipher_alphabet.get_index(char)
            if idx != -1:
                new_idx = idx ^ mask[i]
                unmasked_chars.append(self.current_cipher_alphabet.get_symbol(new_idx))
            else:
                unmasked_chars.append(char)

        rng = CSPRNG(key_params['seed'])

        plaintext = []
        pos = 0
        cipher_size = len(self.current_cipher_alphabet)

        while pos < total_chars:
            y = rng.get_int(cipher_size)
            has_salt = rng.get_int(1000) < (key_params['salt_prob'] * 1000)

            if has_salt:
                salt_pos = self.choose_salt_position(rng, key_params['weights'])
                salt = rng.get_int(cipher_size)

                if pos + 2 >= total_chars:
                    break

                if salt_pos == 0:
                    pos += 1
                    if pos >= total_chars:
                        break
                    char_x = unmasked_chars[pos]
                    x_index = self.current_cipher_alphabet.get_index(char_x)
                    pos += 2

                elif salt_pos == 1:
                    if pos >= total_chars:
                        break
                    char_x = unmasked_chars[pos]
                    x_index = self.current_cipher_alphabet.get_index(char_x)
                    pos += 3

                else:
                    if pos >= total_chars:
                        break
                    char_x = unmasked_chars[pos]
                    x_index = self.current_cipher_alphabet.get_index(char_x)
                    pos += 3
            else:
                if pos + 1 >= total_chars:
                    break

                if pos >= total_chars:
                    break
                char_x = unmasked_chars[pos]
                x_index = self.current_cipher_alphabet.get_index(char_x)
                pos += 2

            if x_index != -1 and 0 <= x_index < len(source_alphabet):
                plaintext.append(source_alphabet[x_index])
            else:
                plaintext.append('?')

        result = ''.join(plaintext)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, result)

        self.src_len_label.config(text=str(total_chars))
        self.res_len_label.config(text=str(len(plaintext)))
        self.status.config(text=f"Decrypted {len(plaintext)} characters out of {total_chars} (with XOR)")

    def clear_all(self):
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.src_len_label.config(text="0")
        self.res_len_label.config(text="0")
        self.status.config(text="Cleared")

    def load_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(tk.END, content)
                self.status.config(text=f"Loaded {filename}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            try:
                content = self.output_text.get(1.0, tk.END).strip()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.status.config(text=f"Saved {filename}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def show_about(self):
        messagebox.showinfo("About",
                            "Absoluta\n"
                            "Version 0.1.0")


if __name__ == "__main__":
    root = tk.Tk()
    app = RetroCipherApp(root)
    root.mainloop()