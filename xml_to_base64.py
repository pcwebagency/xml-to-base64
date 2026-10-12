#!/usr/bin/env python3
"""GUI per convertire file XML o XML.p7m in base64."""

import base64
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

EXTENSIONS_SUPPORTATE = (".xml", ".p7m")
AUTORE = "Ing. Carmine Palermo"


class XmlToBase64App:
    def __init__(self, root):
        self.root = root
        self.root.title("XML/P7M → Base64")
        self.root.geometry("800x650")
        self.root.minsize(600, 450)

        self.file_path = None
        self._build_ui()
        self._build_menu()

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Informazioni...", command=self.mostra_info)
        menubar.add_cascade(label="Info", menu=help_menu)

        self.root.config(menu=menubar)

    def mostra_info(self):
        messagebox.showinfo(
            "Informazioni",
            f"XML/P7M → Base64\n\nSviluppato da {AUTORE}",
        )

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        # Riga upload
        top = ttk.Frame(main)
        top.pack(fill=tk.X, pady=(0, 10))

        self.btn_upload = ttk.Button(top, text="Carica file...", command=self.carica_file)
        self.btn_upload.pack(side=tk.LEFT)

        self.lbl_file = ttk.Label(top, text="Nessun file selezionato", foreground="gray")
        self.lbl_file.pack(side=tk.LEFT, padx=10)

        # Area testo input (incolla testo da codificare/decodificare)
        ttk.Label(main, text="Testo (incolla qui per codificare/decodificare):").pack(anchor=tk.W)

        self.txt_input = scrolledtext.ScrolledText(main, wrap=tk.CHAR, font=("Menlo", 11), height=8)
        self.txt_input.pack(fill=tk.BOTH, expand=True, pady=(5, 5))

        # Riga pulsanti codifica/decodifica/cancella
        actions = ttk.Frame(main)
        actions.pack(fill=tk.X, pady=(0, 10))

        self.btn_encode = ttk.Button(actions, text="Codifica", command=self.codifica_testo)
        self.btn_encode.pack(side=tk.LEFT)

        self.btn_decode = ttk.Button(actions, text="Decodifica", command=self.decodifica_testo)
        self.btn_decode.pack(side=tk.LEFT, padx=(10, 0))

        self.btn_clear = ttk.Button(actions, text="Cancella", command=self.cancella_tutto)
        self.btn_clear.pack(side=tk.LEFT, padx=(10, 0))

        # Area testo risultato
        ttk.Label(main, text="Risultato Base64:").pack(anchor=tk.W)

        self.txt_output = scrolledtext.ScrolledText(main, wrap=tk.CHAR, font=("Menlo", 11))
        self.txt_output.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        # Riga azioni + status
        bottom = ttk.Frame(main)
        bottom.pack(fill=tk.X)

        self.btn_copy = ttk.Button(bottom, text="Copia negli appunti", command=self.copia_clipboard, state=tk.DISABLED)
        self.btn_copy.pack(side=tk.LEFT)

        self.btn_export = ttk.Button(bottom, text="Esporta su file...", command=self.esporta_file, state=tk.DISABLED)
        self.btn_export.pack(side=tk.LEFT, padx=(10, 0))

        self.lbl_status = ttk.Label(bottom, text="", foreground="green")
        self.lbl_status.pack(side=tk.RIGHT)

  

    def codifica_testo(self):
        testo = self.txt_input.get("1.0", tk.END).rstrip("\n")
        if not testo:
            messagebox.showinfo("Nessun testo", "Incolla del testo nel riquadro di input prima di codificare.")
            return

        b64 = base64.b64encode(testo.encode("utf-8")).decode("ascii")

        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, b64)

        self.btn_copy.config(state=tk.NORMAL)
        self.btn_export.config(state=tk.NORMAL)
        self.lbl_status.config(text=f"Codificati {len(testo)} caratteri → {len(b64)} caratteri base64")

    def decodifica_testo(self):
        testo = self.txt_input.get("1.0", tk.END).strip()
        if not testo:
            messagebox.showinfo("Nessun testo", "Incolla del testo base64 nel riquadro di input prima di decodificare.")
            return

        try:
            decoded_bytes = base64.b64decode(testo, validate=True)
        except (base64.binascii.Error, ValueError) as e:
            messagebox.showerror("Errore decodifica", f"Il testo non è un base64 valido.\n{e}")
            return

        try:
            decoded = decoded_bytes.decode("utf-8")
        except UnicodeDecodeError:
            decoded = decoded_bytes.decode("utf-8", errors="replace")
            messagebox.showwarning(
                "Decodifica parziale",
                "Il contenuto decodificato non è testo UTF-8 valido; alcuni caratteri sono stati sostituiti.",
            )

        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, decoded)

        self.btn_copy.config(state=tk.NORMAL)
        self.btn_export.config(state=tk.NORMAL)
        self.lbl_status.config(text=f"Decodificati {len(testo)} caratteri base64 → {len(decoded)} caratteri")

    def cancella_tutto(self):
        self.txt_input.delete("1.0", tk.END)
        self.txt_output.delete("1.0", tk.END)
        self.file_path = None
        self.lbl_file.config(text="Nessun file selezionato", foreground="gray")
        self.btn_copy.config(state=tk.DISABLED)
        self.btn_export.config(state=tk.DISABLED)
        self.lbl_status.config(text="")

    def carica_file(self):
        path = filedialog.askopenfilename(
            title="Seleziona file XML o P7M",
            filetypes=[
                ("File supportati", "*.xml *.p7m"),
                ("File XML", "*.xml"),
                ("File P7M", "*.p7m"),
                ("Tutti i file", "*.*"),
            ],
        )
        if not path:
            return

        ext = os.path.splitext(path)[1].lower()
        if ext not in EXTENSIONS_SUPPORTATE:
            if not messagebox.askyesno(
                "Estensione non riconosciuta",
                f"Il file selezionato ha estensione '{ext}', non .xml o .p7m.\n"
                "Vuoi convertirlo comunque?",
            ):
                return

        try:
            with open(path, "rb") as f:
                contenuto = f.read()
        except OSError as e:
            messagebox.showerror("Errore lettura file", str(e))
            return

        b64 = base64.b64encode(contenuto).decode("ascii")

        self.file_path = path
        self.lbl_file.config(text=os.path.basename(path), foreground="black")

        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, b64)

        self.btn_copy.config(state=tk.NORMAL)
        self.btn_export.config(state=tk.NORMAL)
        self.lbl_status.config(text=f"Convertiti {len(contenuto)} byte → {len(b64)} caratteri base64")

    def copia_clipboard(self):
        testo = self.txt_output.get("1.0", tk.END).strip()
        if not testo:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(testo)
        self.lbl_status.config(text="Copiato negli appunti!")

    def esporta_file(self):
        testo = self.txt_output.get("1.0", tk.END).strip()
        if not testo:
            return

        nome_base = os.path.splitext(os.path.basename(self.file_path))[0] if self.file_path else "output"
        path = filedialog.asksaveasfilename(
            title="Esporta base64 su file",
            defaultextension=".txt",
            initialfile=f"{nome_base}_base64.txt",
            filetypes=[("File di testo", "*.txt"), ("Tutti i file", "*.*")],
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="ascii") as f:
                f.write(testo)
        except OSError as e:
            messagebox.showerror("Errore salvataggio file", str(e))
            return

        self.lbl_status.config(text=f"Esportato in {os.path.basename(path)}")


def main():
    root = tk.Tk()
    app = XmlToBase64App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
