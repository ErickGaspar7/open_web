import os
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Open Web")
        self.root.geometry("300x450")  # Tamanho aumentado
        self.root.resizable(False, False)  # Não permite redimensionar a janela
        self.root.configure(bg="#f2f2f2")  # Cor de fundo moderna

        # Adicionando ícone personalizado
        self.root.iconbitmap("ico.ico")

        # Centraliza a janela na tela
        self.centralizar_janela()

        # Lista para armazenar os links
        self.sites = self.carregar_sites()

        # Título
        self.label_title = ttk.Label(
            root,
            text="Open Web",
            font=("Segoe UI", 16, "bold"),
            background="#f2f2f2",
            foreground="#1e1e1e",
        )
        self.label_title.pack(pady=(10, 10))

        # Campo de entrada para o nome do site
        self.entry_name = ttk.Entry(root, width=25, font=("Segoe UI", 12), justify="center")
        self.entry_name.pack(pady=(5, 10))
        self.set_placeholder(self.entry_name, "Nome do site")

        # Campo de entrada para o URL do site
        self.entry_url = ttk.Entry(root, width=25, font=("Segoe UI", 12), justify="center")
        self.entry_url.pack(pady=(5, 15))
        self.set_placeholder(self.entry_url, "URL do site")

        # Lista para exibir os links adicionados
        self.listbox_label = ttk.Label(
            root,
            text="Sites Adicionados:",
            font=("Segoe UI", 12, "bold"),
            background="#f2f2f2",
            foreground="#1e1e1e",
        )
        self.listbox_label.pack(pady=(10, 5))

        # Listbox com barra de rolagem
        self.listbox_frame = ttk.Frame(root)
        self.listbox_frame.pack(pady=(5, 15))

        self.listbox = tk.Listbox(
            self.listbox_frame,
            width=35,
            height=6,
            font=("Segoe UI", 10),
            selectmode=tk.SINGLE,
            bd=0,
            highlightthickness=0,
        )
        self.listbox.grid(row=0, column=0, padx=5, pady=5)

        self.scrollbar = ttk.Scrollbar(self.listbox_frame, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Botões organizados em uma linha
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(pady=(10, 0))

        self.add_button = ttk.Button(self.button_frame, text="+", command=self.adicionar_site, width=5)
        self.add_button.grid(row=5, column=0, padx=(5, 5))

        self.open_button = ttk.Button(self.button_frame, text="✓", command=self.abrir_sites, width=5)
        self.open_button.grid(row=5, column=1, padx=(5, 5))

        self.delete_button = ttk.Button(self.button_frame, text="X", command=self.excluir_site, width=5)
        self.delete_button.grid(row=5, column=2, padx=(5, 5))

        # Carregar os sites na interface
        self.atualizar_lista()

        # Número de versão com margem inferior
        self.label_version = ttk.Label(
            root,
            text="Versão 1.0",
            font=("Segoe UI", 8),
            background="#f2f2f2",
            foreground="#1e1e1e",
        )
        self.label_version.pack(side="bottom", pady=(10, 25))

    def set_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)
        entry.config(foreground="gray")
        entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, entry, placeholder))
        entry.bind("<FocusOut>", lambda event: self.restore_placeholder(event, entry, placeholder))

    def clear_placeholder(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(foreground="black")

    def restore_placeholder(self, event, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(foreground="gray")

    def adicionar_site(self):
        nome = self.entry_name.get()
        url = self.entry_url.get()

        if nome == "Nome do site" or url == "URL do site":
            messagebox.showwarning("Aviso", "Preencha todos os campos antes de adicionar!")
            return

        if nome and url:
            site = (nome, url)
            self.sites.append(site)
            self.listbox.insert(tk.END, f"{nome} - {url}")
            self.salvar_sites()
            self.entry_name.delete(0, tk.END)
            self.entry_url.delete(0, tk.END)
            self.restore_placeholder(None, self.entry_name, "Nome do site")
            self.restore_placeholder(None, self.entry_url, "URL do site")

    def excluir_site(self):
        try:
            selected_index = self.listbox.curselection()[0]
            self.listbox.delete(selected_index)
            del self.sites[selected_index]
            self.salvar_sites()
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um site para excluir!")

    def abrir_sites(self):
        for _, site in self.sites:
            try:
                webbrowser.open(site)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir o site {site}: {e}")

    def carregar_sites(self):
        try:
            # Usando o diretório apropriado para salvar e carregar os sites
            user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Open Web")
            os.makedirs(user_data_dir, exist_ok=True)
            sites_file = os.path.join(user_data_dir, "sites.txt")

            with open(sites_file, "r") as file:
                sites = [line.strip().split('|') for line in file.readlines()]
            return [(nome, url) for nome, url in sites]
        except FileNotFoundError:
            return []

    def salvar_sites(self):
        try:
            # Usando o diretório apropriado para salvar os sites
            user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Open Web")
            os.makedirs(user_data_dir, exist_ok=True)
            sites_file = os.path.join(user_data_dir, "sites.txt")

            with open(sites_file, "w") as file:
                for nome, url in self.sites:
                    file.write(f"{nome}|{url}\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar os sites: {e}")

    def atualizar_lista(self):
        for nome, url in self.sites:
            self.listbox.insert(tk.END, f"{nome} - {url}")

    def centralizar_janela(self):
        window_width = 300
        window_height = 450
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)

    style = ttk.Style()
    style.configure(
        "TButton",
        font=("Segoe UI", 10),
        padding=5,
        relief="flat",
        background="#0078d4",
        foreground="black",
    )
    style.map("TButton", background=[("active", "#005a8b")])

    root.mainloop()
