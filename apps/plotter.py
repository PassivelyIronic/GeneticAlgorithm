import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

class Plotter:
    """
    Klasa odpowiedzialna za rysowanie wykresów związanych z algorytmem genetycznym.
    """
    
    def __init__(self):
        """Inicjalizacja obiektu Plotter."""
        self.output_dir = "results"
        # Upewnij się, że folder na wyniki istnieje
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def plot_fitness_history(self, best_fitness_history, avg_fitness_history, save=True, show=True):
        """
        Rysuje wykres historii przystosowania najlepszego osobnika i średniego przystosowania populacji.
        
        Args:
            best_fitness_history (list): Historia najlepszego przystosowania
            avg_fitness_history (list): Historia średniego przystosowania
            save (bool): Czy zapisać wykres do pliku
            show (bool): Czy wyświetlić wykres
            
        Returns:
            str: Ścieżka do zapisanego pliku (jeśli save=True)
        """
        plt.figure(figsize=(10, 6))
        generations = list(range(len(best_fitness_history)))
        
        plt.plot(generations, best_fitness_history, 'b-', label='Najlepsze przystosowanie')
        plt.plot(generations, avg_fitness_history, 'r-', label='Średnie przystosowanie')
        
        plt.xlabel('Pokolenie')
        plt.ylabel('Przystosowanie')
        plt.title('Historia przystosowania populacji')
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
    
    def plot_convergence(self, best_fitness_history, save=True, show=True):
        """
        Rysuje wykres zbieżności algorytmu genetycznego.
        
        Args:
            best_fitness_history (list): Historia najlepszego przystosowania
            save (bool): Czy zapisać wykres do pliku
            show (bool): Czy wyświetlić wykres
            
        Returns:
            str: Ścieżka do zapisanego pliku (jeśli save=True)
        """
        plt.figure(figsize=(10, 6))
        
        # Obliczamy zmianę przystosowania w kolejnych pokoleniach
        changes = [abs(best_fitness_history[i] - best_fitness_history[i-1]) 
                  for i in range(1, len(best_fitness_history))]
        
        plt.semilogy(range(1, len(best_fitness_history)), changes)
        plt.xlabel('Pokolenie')
        plt.ylabel('Zmiana najlepszego przystosowania (skala logarytmiczna)')
        plt.title('Zbieżność algorytmu genetycznego')
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
    
    def plot_best_individual(self, best_individual, bounds, resolution=100, save=True, show=True):
        """
        Rysuje wykres wartości funkcji celu dla najlepszego osobnika (dla problemów dwuwymiarowych).
        
        Args:
            best_individual: Najlepszy osobnik
            bounds: Granice dla zmiennych
            resolution: Rozdzielczość wykresu
            save (bool): Czy zapisać wykres do pliku
            show (bool): Czy wyświetlić wykres
            
        Returns:
            str: Ścieżka do zapisanego pliku (jeśli save=True)
        """
        # Sprawdzamy, czy problem jest dwuwymiarowy
        if len(best_individual.chromosome_values) != 2:
            print("Wykres wartości funkcji celu można narysować tylko dla problemu dwuwymiarowego")
            return None
        
        # Przygotowujemy siatkę punktów
        x = np.linspace(bounds[0][0], bounds[0][1], resolution)
        y = np.linspace(bounds[1][0], bounds[1][1], resolution)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # Obliczamy wartość funkcji celu dla każdego punktu siatki
        for i in range(resolution):
            for j in range(resolution):
                # Tworzymy punkt [x, y]
                point = [X[i, j], Y[i, j]]
                
                # Obliczamy wartość funkcji celu dla tego punktu
                # Zakładamy, że mamy dostęp do funkcji fitness
                from algorithms.fitness import evaluate_fitness
                Z[i, j] = evaluate_fitness(point)
        
        # Rysujemy wykres 3D
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
        
        # Zaznaczamy najlepszy punkt
        ax.scatter(best_individual.chromosome_values[0], 
                   best_individual.chromosome_values[1], 
                   best_individual.fitness, 
                   color='red', s=100, label='Najlepszy punkt')
        
        ax.set_xlabel('x1')
        ax.set_ylabel('x2')
        ax.set_zlabel('Wartość funkcji celu')
        ax.set_title('Powierzchnia funkcji celu z najlepszym znalezionym punktem')
        fig.colorbar(surf)
        ax.legend()
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.output_dir, f"best_individual_{timestamp}.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Zapisano wykres do pliku: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return filepath if save else None