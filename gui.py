import tkinter as tk
from tkinter import ttk, scrolledtext
import time
from PIL import Image, ImageTk

class AlarmGUI:
    def __init__(self, monitor):
        self.monitor = monitor
        self.root = tk.Tk()
        self.root.title("Mixer Sonoro de Alarmes")
        self.root.geometry("600x650")
        self.root.resizable(True, True)  # janela com tamanho fixo

        # Troca o ícone da janela
        try:
            icone = ImageTk.PhotoImage(file="ouvindo.png")
            self.root.iconphoto(True, icone)
        except Exception as e:
            print(f"Não foi possível carregar o ícone: {e}")

        self.status_labels = {}
        self._create_widgets()
        self.monitor.gui_callback = self.update_alarm_status
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Player de Alarmes", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))

        # ---------- LISTA DE ALARMES COM SCROLL ----------
        alarm_frame = ttk.LabelFrame(main_frame, text="Status dos Alarmes", padding="5")
        alarm_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Canvas e Scrollbar
        canvas = tk.Canvas(alarm_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(alarm_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno que conterá os alarmes
        inner_frame = ttk.Frame(canvas)

        # Coloca o frame interno dentro do canvas
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Empacota canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Cabeçalho (dentro do inner_frame)
        header_frame = ttk.Frame(inner_frame)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(header_frame, text="Alarme", font=("Arial", 10, "bold"), width=30).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text="Status", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)

        # Cria uma linha para cada alarme dentro do inner_frame
        for alarm in self.monitor.alarms:
            row_frame = ttk.Frame(inner_frame)
            row_frame.pack(fill=tk.X, pady=2)

            lbl_name = ttk.Label(row_frame, text=alarm['name'], width=30, anchor="w")
            lbl_name.pack(side=tk.LEFT, padx=5)

            lbl_status = ttk.Label(row_frame, text="Inativo", foreground="green", width=15)
            lbl_status.pack(side=tk.LEFT, padx=5)

            self.status_labels[alarm['name']] = lbl_status

        # Atualiza a região rolável quando o inner_frame mudar de tamanho
        def _configure_inner_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner_frame.bind("<Configure>", _configure_inner_frame)

        # ---------- LOG DE EVENTOS ----------
        log_frame = ttk.LabelFrame(main_frame, text="Log de Eventos", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, state='disabled', wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # ---------- BOTÕES ----------
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Limpar Log", command=self.limpar_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Sair", command=self.on_close).pack(side=tk.RIGHT, padx=5)

        # ---------- STATUS DO SERVIDOR MODBUS ----------
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(5, 5))
        self.status_server_label = ttk.Label(
            status_frame,
            text="✅ Servidor Modbus: Ativo",
            font=("Arial", 9),
            foreground="green"
        )
        self.status_server_label.pack(anchor='center')

        # ---------- CRÉDITO (RODAPÉ) ----------
        credito_frame = ttk.Frame(main_frame)
        credito_frame.pack(fill=tk.X, pady=(0, 0))
        ttk.Label(credito_frame, text="© Desenvolvido por Thiago Alves",
                  font=("Arial", 8), foreground="gray").pack(anchor='center')

    def update_alarm_status(self, alarm_name, is_active):
        if alarm_name in self.status_labels:
            lbl = self.status_labels[alarm_name]
            if is_active:
                lbl.config(text="ATIVO", foreground="red")
                self.log(f"{alarm_name} -> ATIVO")   # só loga quando ativa
            else:
                lbl.config(text="Inativo", foreground="green")
                # Não adiciona log para inativo

    def log(self, message):
        self.log_text.config(state='normal')
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def limpar_log(self):
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')

    def on_close(self):
        self.monitor.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()