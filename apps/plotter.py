import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class Plotter:
    
    def __init__(self):
        self.output_dir = "results"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        self.best_fitness_history = []
        self.avg_fitness_history = []
        
    def update_history(self, best_fitness, avg_fitness=None):
        self.best_fitness_history.append(best_fitness)
        if avg_fitness is not None:
            self.avg_fitness_history.append(avg_fitness)
    
    def plot_fitness_history(self, title="Historia wartości funkcji celu", save=True, show=True):
        fig = plt.figure(figsize=(10, 6))
        generations = list(range(len(self.best_fitness_history)))
        
        plt.plot(generations, self.best_fitness_history, 'b-', label='Najlepsze przystosowanie')
        
        if self.avg_fitness_history:
            plt.plot(generations, self.avg_fitness_history, 'r-', label='Średnie przystosowanie')
        
        plt.xlabel('Iteracja')
        plt.ylabel('Wartość funkcji celu')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.output_dir, f"fitness_history_{timestamp}.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Zapisano wykres do pliku: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return filepath if save else None
    
    def plot_convergence(self, title="Zbieżność algorytmu genetycznego", save=True, show=True):

        if len(self.best_fitness_history) < 2:
            print("Za mało danych do wygenerowania wykresu zbieżności")
            return None
        
        fig = plt.figure(figsize=(10, 6))
        
        changes = [abs(self.best_fitness_history[i] - self.best_fitness_history[i-1]) 
                  for i in range(1, len(self.best_fitness_history))]
        
        plt.semilogy(range(1, len(self.best_fitness_history)), changes)
        plt.xlabel('Iteracja')
        plt.ylabel('Zmiana najlepszego przystosowania (skala logarytmiczna)')
        plt.title(title)
        plt.grid(True)
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.output_dir, f"convergence_{timestamp}.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Zapisano wykres do pliku: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return filepath if save else None
    
    def plot_function_landscape(self, best_point, fitness_func, bounds, title="Powierzchnia funkcji celu", resolution=50, save=True, show=True):

        if len(best_point) != 2:
            print("Funkcja krajobrazowa może być narysowana tylko dla funkcji dwuwymiarowych")
            return None
        
        x_min, x_max = bounds
        
        x = np.linspace(x_min, x_max, resolution)
        y = np.linspace(x_min, x_max, resolution)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        for i in range(resolution):
            for j in range(resolution):
                from algorithms.individual import Individual
                temp_ind = Individual(num_variables=2, precision=5, random_init=False)
                temp_ind.chromosome_values = [X[i, j], Y[i, j]]
                Z[i, j] = fitness_func(temp_ind)
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
        
        best_x, best_y = best_point
        from algorithms.individual import Individual
        temp_ind = Individual(num_variables=2, precision=5, random_init=False)
        temp_ind.chromosome_values = [best_x, best_y]
        best_z = fitness_func(temp_ind)
        
        ax.scatter(best_x, best_y, best_z, color='red', s=100, marker='*', label='Najlepszy punkt')
        
        ax.set_xlabel('x1')
        ax.set_ylabel('x2')
        ax.set_zlabel('Wartość funkcji celu')
        ax.set_title(title)
        fig.colorbar(surf)
        ax.legend()
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.output_dir, f"function_landscape_{timestamp}.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Zapisano wykres do pliku: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return filepath if save else None
            
    def show_results_window(self, best_individual, execution_time):

        results_window = tk.Toplevel()
        results_window.title("Wyniki Algorytmu Genetycznego")
        results_window.geometry("800x600")
        
        main_frame = tk.Frame(results_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        results_frame = tk.Frame(main_frame)
        results_frame.pack(fill=tk.X, pady=10)
        
        results_text = (
            f"Najlepsze rozwiązanie: {best_individual.chromosome_values}\n"
            f"Wartość funkcji celu: {best_individual.fitness}\n"
            f"Czas wykonania: {execution_time:.2f} sekund"
        )
        
        results_label = tk.Label(results_frame, text=results_text, justify=tk.LEFT, font=("Arial", 12))
        results_label.pack(anchor=tk.W)
        
        chart_frame = tk.Frame(main_frame)
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        fig = Figure(figsize=(8, 4), dpi=100)
        plot = fig.add_subplot(111)
        
        generations = list(range(len(self.best_fitness_history)))
        plot.plot(generations, self.best_fitness_history, 'b-', label='Najlepsze przystosowanie')
        
        if self.avg_fitness_history:
            plot.plot(generations, self.avg_fitness_history, 'r-', label='Średnie przystosowanie')
        
        plot.set_xlabel('Iteracja')
        plot.set_ylabel('Wartość funkcji celu')
        plot.set_title('Historia wartości funkcji celu')
        plot.grid(True)
        plot.legend()
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        save_button = tk.Button(buttons_frame, text="Zapisz wykres", 
                               command=lambda: self.plot_fitness_history(save=True, show=False))
        save_button.pack(side=tk.LEFT, padx=5)
        
        show_more_button = tk.Button(buttons_frame, text="Pokaż więcej wykresów", 
                                    command=lambda: self.plot_convergence(save=False, show=True))
        show_more_button.pack(side=tk.LEFT, padx=5)
        
        close_button = tk.Button(buttons_frame, text="Zamknij", command=results_window.destroy)
        close_button.pack(side=tk.RIGHT, padx=5)