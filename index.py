import numpy as np
import tkinter as tk
from tkinter import ttk
import threading
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as mcolors
from concurrent.futures import ThreadPoolExecutor

class JogoDaVida:
    def __init__(self, N=50, num_threads=4):
        self.N = N
        self.num_threads = num_threads
        self.grid = self._create_initial_grid()
        self.running = False
        self.speed = 200  # ms
        self.thread_colors = self._generate_thread_colors()
        self.thread_pool = ThreadPoolExecutor(max_workers=num_threads)
        self.setup_gui()
        
    def _create_initial_grid(self):
        """Cria um grid inicial com células aleatórias"""
        return np.random.choice([0, 1], self.N*self.N, p=[0.85, 0.15]).reshape(self.N, self.N)
    
    def _generate_thread_colors(self):
        """Gera cores distintas para cada thread"""
        base_colors = list(mcolors.TABLEAU_COLORS.values())
        colors = []
        for color in base_colors:
            # Criar uma versão mais clara da cor para melhor visualização
            rgb = mcolors.to_rgb(color)
            lighter_color = [min(1.0, c * 1.5) for c in rgb]
            colors.append(lighter_color)
        return colors[:self.num_threads]

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Jogo da Vida - Simulação Paralela")
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame para informações
        info_frame = ttk.LabelFrame(main_frame, text="Regras", padding="5")
        info_frame.grid(row=0, column=0, columnspan=5, pady=(0, 10), sticky=(tk.W, tk.E))
        
        rules_text = """
        • Sobrevivência: Célula viva com 2 ou 3 vizinhos vivos permanece viva
        • Nascimento: Célula morta com exatamente 3 vizinhos vivos torna-se viva
        • Morte: Nos demais casos, a célula morre ou continua morta
        """
        ttk.Label(info_frame, text=rules_text, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
        
        # Configuração do plot
        self.fig = Figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=5)
        
        # Frame para controles
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=5, pady=10)
        
        # Botões e controles
        self.btn_start = ttk.Button(control_frame, text="Iniciar", command=self.toggle_simulation)
        self.btn_start.grid(row=0, column=0, padx=5)
        
        ttk.Label(control_frame, text="Velocidade:").grid(row=0, column=1, padx=5)
        self.speed_scale = ttk.Scale(control_frame, from_=50, to=500, orient=tk.HORIZONTAL,
                                   command=self.update_speed)
        self.speed_scale.set(self.speed)
        self.speed_scale.grid(row=0, column=2, padx=5)
        
        self.btn_clear = ttk.Button(control_frame, text="Limpar", command=self.clear_grid)
        self.btn_clear.grid(row=0, column=3, padx=5)
        
        self.btn_reset = ttk.Button(control_frame, text="Reset", command=self.reset_grid)
        self.btn_reset.grid(row=0, column=4, padx=5)
        
        # Status das threads
        self.thread_status = ttk.Label(main_frame, text="Threads: Aguardando")
        self.thread_status.grid(row=3, column=0, columnspan=5, pady=5)
        
        # Configuração inicial do plot
        self.img = self.ax.imshow(self.grid, interpolation='nearest')
        self.canvas.draw()
        
        # Adicionar evento de clique
        self.canvas.mpl_connect('button_press_event', self.on_click)
        
        # Inicializar visualização das threads
        self.thread_visualization = np.zeros_like(self.grid)
        self._update_thread_visualization()

    def atualizar_regiao(self, start_row, end_row, novo_grid):
        """Atualiza uma região específica do grid, incluindo bordas compartilhadas"""
        # Incluir uma linha extra em cada direção para bordas
        start_row_with_border = max(0, start_row - 1)
        end_row_with_border = min(self.N, end_row + 1)
        
        for i in range(start_row_with_border, end_row_with_border):
            for j in range(self.N):
                # Calcula vizinhos considerando as bordas toroidais
                vizinhos = [
                    self.grid[(i-1)%self.N, (j-1)%self.N], self.grid[(i-1)%self.N, j], self.grid[(i-1)%self.N, (j+1)%self.N],
                    self.grid[i, (j-1)%self.N],                                       self.grid[i, (j+1)%self.N],
                    self.grid[(i+1)%self.N, (j-1)%self.N], self.grid[(i+1)%self.N, j], self.grid[(i+1)%self.N, (j+1)%self.N]
                ]
                total = sum(vizinhos)
                
                # Aplicar regras do Jogo da Vida
                if self.grid[i, j] == 1:  # Célula viva
                    novo_grid[i, j] = 1 if total in [2, 3] else 0
                else:  # Célula morta
                    novo_grid[i, j] = 1 if total == 3 else 0
        
        return start_row, end_row  # Retorna região processada para visualização

    def atualizar(self):
        """Atualiza o grid usando múltiplas threads com gestão de bordas"""
        novo_grid = np.zeros_like(self.grid)
        rows_per_thread = self.N // self.num_threads
        futures = []
        
        # Submete tarefas para o thread pool
        for i in range(self.num_threads):
            start_row = i * rows_per_thread
            end_row = start_row + rows_per_thread if i < self.num_threads - 1 else self.N
            future = self.thread_pool.submit(self.atualizar_regiao, start_row, end_row, novo_grid)
            futures.append(future)
        
        # Aguarda todas as threads terminarem
        for future in futures:
            future.result()
        
        self.grid = novo_grid
        self._update_thread_status("Processando")

    def _update_thread_status(self, status):
        """Atualiza o status das threads na interface"""
        self.thread_status.config(text=f"Threads: {status} ({self.num_threads} threads ativas)")

    def run_simulation(self):
        """Executa a simulação em loop"""
        while self.running:
            self.atualizar()
            self._update_display()
            time.sleep(self.speed / 1000)
        self._update_thread_status("Aguardando")

    def toggle_simulation(self):
        """Alterna entre iniciar e parar a simulação"""
        self.running = not self.running
        self.btn_start.config(text="Parar" if self.running else "Iniciar")
        if self.running:
            threading.Thread(target=self.run_simulation, daemon=True).start()
            self._update_thread_status("Iniciando")
        else:
            self._update_thread_status("Parado")

    def reset_grid(self):
        """Reseta o grid para um novo estado aleatório"""
        self.grid = self._create_initial_grid()
        self._update_display()
        self._update_thread_status("Reset")

    def clear_grid(self):
        """Limpa o grid (todas as células mortas)"""
        self.grid = np.zeros((self.N, self.N))
        self._update_display()
        self._update_thread_status("Limpo")

    def on_click(self, event):
        """Manipula eventos de clique na grade"""
        if event.inaxes == self.ax:
            x, y = int(event.ydata), int(event.xdata)
            if 0 <= x < self.N and 0 <= y < self.N:
                self.grid[x, y] = 1 - self.grid[x, y]
                self._update_display()

    def update_speed(self, value):
        """Atualiza a velocidade da simulação"""
        self.speed = int(float(value))

    def _update_thread_visualization(self):
        """Atualiza a visualização das áreas processadas por cada thread"""
        rows_per_thread = self.N // self.num_threads
        for i in range(self.num_threads):
            start_row = i * rows_per_thread
            end_row = start_row + rows_per_thread if i < self.num_threads - 1 else self.N
            self.thread_visualization[start_row:end_row] = i

    def _update_display(self):
        """Atualiza a exibição do grid com cores das threads e células"""
        grid_display = np.zeros((self.N, self.N, 4))
        
        # Adiciona cores das threads como overlay
        for i in range(self.num_threads):
            mask = self.thread_visualization == i
            color = mcolors.to_rgba(self.thread_colors[i], alpha=0.2)
            grid_display[mask] = color
        
        # Adiciona células vivas
        alive_mask = self.grid == 1
        grid_display[alive_mask] = mcolors.to_rgba('black')
        
        self.img.set_array(grid_display)
        self.canvas.draw_idle()

    def iniciar(self):
        """Inicia a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    jogo = JogoDaVida(50, num_threads=4)
    jogo.iniciar()