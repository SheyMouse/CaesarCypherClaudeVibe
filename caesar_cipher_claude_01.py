import tkinter as tk
from tkinter import ttk, messagebox


def caesar_cipher(text, shift, encrypt=True):
    if not encrypt:
        shift = -shift
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)


def do_encrypt():
    message = input_text.get("1.0", tk.END).strip()
    if not message:
        messagebox.showwarning("No Message", "Please enter a message to encrypt.")
        return
    try:
        shift = int(shift_var.get())
    except ValueError:
        messagebox.showerror("Invalid Key", "Shift key must be a whole number.")
        return
    result = caesar_cipher(message, shift, encrypt=True)
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", result)
    output_text.config(state="disabled")


def do_decrypt():
    message = output_text.get("1.0", tk.END).strip()
    if not message:
        messagebox.showwarning("No Message", "Please enter or encrypt some cypher text first.")
        return
    try:
        shift = int(shift_var.get())
    except ValueError:
        messagebox.showerror("Invalid Key", "Shift key must be a whole number.")
        return
    result = caesar_cipher(message, shift, encrypt=False)
    input_text.delete("1.0", tk.END)
    input_text.insert("1.0", result)


def copy_encrypted():
    content = output_text.get("1.0", tk.END).strip()
    if content:
        root.clipboard_clear()
        root.clipboard_append(content)
        copy_btn.config(text="\u2713 Copied!")
        root.after(1500, lambda: copy_btn.config(text="Copy Message"))
    else:
        messagebox.showinfo("Nothing to Copy", "Encrypt a message first.")


def paste_message():
    try:
        text = root.clipboard_get()
    except tk.TclError:
        messagebox.showinfo("Nothing to Paste", "The clipboard is empty.")
        return
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", text)


def clear_all():
    input_text.config(state="normal")
    input_text.delete("1.0", tk.END)
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    shift_var.set("3")


def exit_app():
    root.destroy()


def show_help():
    popup = tk.Toplevel(root)
    popup.title("How to Use")
    popup.configure(bg="#1a1a2e")
    popup.resizable(True, True)
    popup.grab_set()

    w, h = 540, 480
    popup.update_idletasks()
    rx = root.winfo_x() + (root.winfo_width() - w) // 2
    ry = root.winfo_y() + (root.winfo_height() - h) // 2
    popup.geometry("%dx%d+%d+%d" % (w, h, rx, ry))
    popup.minsize(400, 300)

    # Header
    hdr = tk.Frame(popup, bg="#e94560", pady=12)
    hdr.pack(fill="x")
    tk.Label(hdr, text="?  HOW TO USE", bg="#e94560", fg="white",
             font=("Georgia", 16, "bold")).pack()

    # Scrollable Text widget
    txt_frame = tk.Frame(popup, bg="#1a1a2e")
    txt_frame.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(txt_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    txt = tk.Text(txt_frame, bg="#1a1a2e", fg="#eaeaea",
                  font=("Courier New", 10),
                  wrap="word", relief="flat", bd=0,
                  padx=20, pady=12, cursor="arrow",
                  yscrollcommand=scrollbar.set,
                  state="normal")
    txt.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=txt.yview)

    def on_mousewheel(event):
        txt.yview_scroll(int(-1 * (event.delta / 120)), "units")
    popup.bind("<MouseWheel>", on_mousewheel)

    # Text tags
    txt.tag_configure("intro",
                      font=("Courier New", 10, "italic"),
                      foreground="#ccccee",
                      lmargin1=10, lmargin2=10,
                      spacing1=4, spacing3=10)
    txt.tag_configure("rule",
                      font=("Courier New", 1),
                      foreground="#333355",
                      background="#333355",
                      spacing3=12)
    txt.tag_configure("heading",
                      font=("Courier New", 11, "bold"),
                      foreground="#e94560",
                      spacing1=14, spacing3=4)
    txt.tag_configure("divider",
                      font=("Courier New", 1),
                      foreground="#0f3460",
                      background="#0f3460",
                      spacing3=4)
    txt.tag_configure("body",
                      font=("Courier New", 10),
                      foreground="#eaeaea",
                      lmargin1=10, lmargin2=10,
                      spacing1=2, spacing3=2)
    txt.tag_configure("example",
                      font=("Courier New", 10, "italic"),
                      foreground="#aaaacc",
                      lmargin1=10, lmargin2=10,
                      spacing1=2, spacing3=2)

    # Intro blurb
    intro = (
        "A Caesar Cipher is one of the oldest encryption techniques. "
        "It works by shifting every letter in a message a fixed number of "
        "places along the alphabet. For example, with a Shift Key of 3, "
        "the word HELLO becomes KHOOR. Anyone who knows the Shift Key can "
        "reverse the process and read the original message."
    )
    txt.insert("end", intro + "\n", "intro")
    txt.insert("end", "\u2500" * 55 + "\n", "rule")

    # How-to sections
    sections = [
        (
            "\U0001f512  Encrypting a Message",
            [
                ("body",    "1.  Type your message in the PLAIN TEXT box on the left."),
                ("body",    "2.  Set a Shift Key using the up/down arrows (e.g. 3)."),
                ("body",    "3.  Click ENCRYPT \u2192 \u2014 your scrambled message appears in the CYPHER TEXT box."),
                ("body",    "4.  Click Copy Encrypted to copy the cypher text to your clipboard."),
                ("body",    "5.  Send the cypher text and the Shift Key number to your recipient."),
            ]
        ),
        (
            "\U0001f513  Decrypting a Message",
            [
                ("body",    "1.  Click CLEAR to reset both fields and unlock the Cypher Text box."),
                ("body",    "2.  Paste or type the cypher text into the CYPHER TEXT box on the right."),
                ("body",    "3.  Set the Shift Key to the same number used when encrypting."),
                ("body",    "4.  Click \u2190 DECRYPT \u2014 the original message appears in the PLAIN TEXT box."),
            ]
        ),
        (
            "\U0001f511  About the Shift Key",
            [
                ("body",    "The Shift Key is a number between -25 and 25."),
                ("body",    "Each letter in your message is shifted that many places through the alphabet."),
                ("example", "Example with Shift Key 3:   A \u2192 D     B \u2192 E     Z \u2192 C"),
                ("body",    "Spaces, numbers, and punctuation are never changed."),
                ("body",    "Both sender and recipient must use the same Shift Key."),
            ]
        ),
        (
            "\u2715  Clearing & Starting Over",
            [
                ("body",    "Click CLEAR at any time to wipe both text fields and reset the Shift Key to 3."),
                ("body",    "After clearing, you can type freely in either text box."),
            ]
        ),
    ]

    for i, (title, points) in enumerate(sections):
        txt.insert("end", title + "\n", "heading")
        txt.insert("end", "\u2500" * 55 + "\n", "divider")
        for tag, line in points:
            txt.insert("end", line + "\n", tag)
        if i < len(sections) - 1:
            txt.insert("end", "\n")

    txt.config(state="disabled")

    # Close button
    tk.Button(popup, text="  Close  ",
              bg="#0f3460", fg="white",
              activebackground="#1a3070", activeforeground="white",
              relief="flat", cursor="hand2",
              font=("Courier New", 10, "bold"), padx=20, pady=8,
              command=popup.destroy).pack(pady=10)


# ── Window ────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Caesar Cipher")
root.resizable(True, True)
root.configure(bg="#1a1a2e")
root.minsize(700, 500)
root.protocol("WM_DELETE_WINDOW", exit_app)

# ── Colours & fonts ───────────────────────────────────────────────────────────
BG      = "#1a1a2e"
CARD    = "#16213e"
ACCENT  = "#e94560"
ACCENT2 = "#0f3460"
TEXT    = "#eaeaea"
MUTED   = "#888"
DIVIDER = "#2a2a4a"
FONT_H   = ("Georgia", 22, "bold")
FONT_LBL = ("Courier New", 10, "bold")
FONT_TXT = ("Courier New", 12)
FONT_BTN = ("Courier New", 11, "bold")

# ── ttk Styles ────────────────────────────────────────────────────────────────
style = ttk.Style()
style.theme_use("clam")
style.configure("TSpinbox",
                fieldbackground=CARD, background=CARD,
                foreground=ACCENT, insertcolor=TEXT, relief="flat",
                font=("Courier New", 20, "bold"),
                arrowcolor=ACCENT, arrowsize=20,
                borderwidth=0, padding=6)
style.map("TSpinbox", fieldbackground=[("readonly", CARD)])

# ── Title ─────────────────────────────────────────────────────────────────────
header = tk.Frame(root, bg=ACCENT, pady=14)
header.pack(fill="x")
tk.Label(header, text="CAESAR CIPHER", bg=ACCENT, fg="white",
         font=FONT_H).pack()
tk.Label(header, text="encrypt \u00b7 send \u00b7 decrypt", bg=ACCENT, fg="white",
         font=("Georgia", 10, "italic")).pack()

# ── Shift key bar ─────────────────────────────────────────────────────────────
key_bar = tk.Frame(root, bg=ACCENT2, pady=14)
key_bar.pack(fill="x")

tk.Label(key_bar, text="SHIFT KEY:", bg=ACCENT2, fg=TEXT,
         font=("Courier New", 12, "bold")).pack(side="left", padx=(20, 10))

shift_var = tk.StringVar(value="3")
spinbox = ttk.Spinbox(key_bar, from_=-25, to=25, textvariable=shift_var,
                      width=4, style="TSpinbox", wrap=True)
spinbox.pack(side="left", ipady=6)

tk.Label(key_bar, text="  \u2190 share this number with your recipient",
         bg=ACCENT2, fg=MUTED, font=("Courier New", 9)).pack(side="left", padx=(10, 0))

exit_btn = tk.Button(key_bar, text="\u23fb  EXIT",
                     bg="#6b1a2a", fg="white",
                     activebackground="#8b2030", activeforeground="white",
                     relief="flat", cursor="hand2",
                     font=("Courier New", 9, "bold"), padx=12, pady=6,
                     command=exit_app)
exit_btn.pack(side="right", padx=(4, 16))

clear_btn_top = tk.Button(key_bar, text="\u2715  CLEAR",
                           bg="#3a1a1a", fg="#ff6b6b",
                           activebackground="#4a2020", activeforeground="#ff9999",
                           relief="flat", cursor="hand2",
                           font=("Courier New", 9, "bold"), padx=12, pady=6,
                           command=clear_all)
clear_btn_top.pack(side="right", padx=(4, 4))

help_btn = tk.Button(key_bar, text="?  HELP",
                     bg="#1a3a1a", fg="#6bff6b",
                     activebackground="#2a4a2a", activeforeground="#99ff99",
                     relief="flat", cursor="hand2",
                     font=("Courier New", 9, "bold"), padx=12, pady=6,
                     command=show_help)
help_btn.pack(side="right", padx=(4, 4))

# ── Two-panel body ────────────────────────────────────────────────────────────
body = tk.Frame(root, bg=BG)
body.pack(fill="both", expand=True)
body.columnconfigure(0, weight=1)
body.columnconfigure(2, weight=1)
body.rowconfigure(0, weight=1)

# ── LEFT: Plain Text ──────────────────────────────────────────────────────────
left = tk.Frame(body, bg=BG)
left.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
left.rowconfigure(1, weight=1)
left.columnconfigure(0, weight=1)
left.columnconfigure(1, weight=1)

tk.Label(left, text="  PLAIN TEXT", bg=BG, fg=MUTED,
         font=FONT_LBL).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))

input_text = tk.Text(left, font=FONT_TXT, bg=CARD, fg=TEXT,
                     insertbackground=TEXT, relief="flat", bd=0,
                     wrap="word", padx=10, pady=8)
input_text.grid(row=1, column=0, columnspan=2, sticky="nsew")

encrypt_btn = tk.Button(left, text="\U0001f512  ENCRYPT \u2192",
                        bg=ACCENT, fg="white",
                        activebackground="#c73652", activeforeground="white",
                        relief="flat", cursor="hand2",
                        font=FONT_BTN, padx=18, pady=10,
                        command=do_encrypt)
encrypt_btn.grid(row=2, column=0, sticky="ew", pady=(10, 0), padx=(0, 4))

copy_btn = tk.Button(left, text="Copy Message",
                     bg="#2a2a4a", fg=MUTED,
                     activebackground="#333", activeforeground=TEXT,
                     relief="flat", cursor="hand2",
                     font=("Courier New", 10, "bold"), padx=10, pady=10,
                     command=copy_encrypted)
copy_btn.grid(row=2, column=1, sticky="ew", pady=(10, 0), padx=(4, 0))

# ── DIVIDER ───────────────────────────────────────────────────────────────────
tk.Frame(body, bg=DIVIDER, width=2).grid(row=0, column=1, sticky="ns", pady=16)

# ── RIGHT: Cypher Text ────────────────────────────────────────────────────────
right = tk.Frame(body, bg=BG)
right.grid(row=0, column=2, sticky="nsew", padx=(8, 16), pady=16)
right.rowconfigure(1, weight=1)
right.columnconfigure(0, weight=1)

tk.Label(right, text="  CYPHER TEXT", bg=BG, fg=MUTED,
         font=FONT_LBL).grid(row=0, column=0, sticky="w", pady=(0, 4))

output_text = tk.Text(right, font=FONT_TXT, bg=CARD, fg=ACCENT,
                      relief="flat", bd=0, wrap="word", padx=10, pady=8,
                      state="disabled")
output_text.grid(row=1, column=0, sticky="nsew")

right_btns = tk.Frame(right, bg=BG)
right_btns.grid(row=2, column=0, sticky="ew", pady=(10, 0))
right_btns.columnconfigure(0, weight=1)
right_btns.columnconfigure(1, weight=1)

decrypt_btn = tk.Button(right_btns, text="\u2190 \U0001f513  DECRYPT",
                        bg=ACCENT2, fg="white",
                        activebackground="#0d2a4f", activeforeground="white",
                        relief="flat", cursor="hand2",
                        font=FONT_BTN, padx=18, pady=10,
                        command=do_decrypt)
decrypt_btn.grid(row=0, column=1, sticky="ew", padx=(4, 0))

paste_btn = tk.Button(right_btns, text="Paste Message",
                      bg="#2a2a4a", fg=MUTED,
                      activebackground="#333", activeforeground=TEXT,
                      relief="flat", cursor="hand2",
                      font=("Courier New", 10, "bold"), padx=10, pady=10,
                      command=paste_message)
paste_btn.grid(row=0, column=0, sticky="ew", padx=(0, 4))

# ── Footer ────────────────────────────────────────────────────────────────────
tk.Label(root, text="Letters are shifted by the key. Spaces & punctuation are preserved.",
         bg=BG, fg=MUTED, font=("Courier New", 8)).pack(pady=(0, 10))

root.mainloop()
