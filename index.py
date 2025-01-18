import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class JogoDaVida:
    def __init__(self, N=50):
        self.N = N
        self.grid = np.random.choice([0, 1], N*N, p=[0.85, 0.15]).reshape(N, N)
    
    def atualizar(self):
        novo_grid = self.grid.copy()
        for i in range(self.N):
            for j in range(self.N):
                total = int((self.grid[i, (j-1)%self.N] + self.grid[i, (j+1)%self.N] + 
                           self.grid[(i-1)%self.N, j] + self.grid[(i+1)%self.N, j] + 
                           self.grid[(i-1)%self.N, (j-1)%self.N] + self.grid[(i-1)%self.N, (j+1)%self.N] + 
                           self.grid[(i+1)%self.N, (j-1)%self.N] + self.grid[(i+1)%self.N, (j+1)%self.N]))
                
                if self.grid[i, j] == 1:
                    if (total < 2) or (total > 3):
                        novo_grid[i, j] = 0
                else:
                    if total == 3:
                        novo_grid[i, j] = 1
        self.grid = novo_grid
        
    def visualizar(self, frames=200):
        fig, ax = plt.subplots()
        img = ax.imshow(self.grid, interpolation='nearest')
        
        def atualizar_animacao(_):
            self.atualizar()
            img.set_array(self.grid)
            return [img]
        
        ani = FuncAnimation(fig, atualizar_animacao, frames=frames, interval=200, blit=True)
        plt.show()

# Exemplo de uso
if __name__ == "__main__":
    jogo = JogoDaVida(50)
    jogo.visualizar()