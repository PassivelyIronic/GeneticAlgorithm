import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from algorithms.config import config 
from algorithms.genetic import run_genetic_algorithm
import os


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

class MainWindow(Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = tk.Tk()
        self.root.title("Genetic Algorithm")
        self.root.geometry("300x375")

        self.selection_methods = ["Best", "Roulette", "Tournament"]
        self.cross_methods = ["single_point", "Two_point", "Uniform"]
        self.mutation_methods = ["single_point", "Two_point", "Edge"]

        main_column = tk.Frame(self.root)
        main_column.pack(padx=10, pady=10)

        defaults = {
            "range_start": config.range_start,
            "range_end": config.range_end,
            "epochs": config.epochs,
            "population_size": config.population_size,
            "precision": config.precision,
            "num_variables": config.num_variables,
            "selection_method": config.selection_method.capitalize(),
            "best_selection_amount": config.best_selection_amount,
            "tournament_size": config.tournament_size,
            "crossover_method": config.crossover_method,
            "crossover_probability": config.crossover_probability,
            "mutation_method": config.mutation_method,
            "mutation_probability": config.mutation_probability,
            "inversion_probability": config.inversion_probability,
            "optimization_type": config.optimization_type
        }

        row1 = tk.Frame(main_column)
        row1.pack(fill="x")
        tk.Label(row1, text="Starting Range").pack(side="left")
        self.range_start_entry = tk.Entry(row1, width=10)
        self.range_start_entry.insert(0, str(defaults["range_start"]))
        self.range_start_entry.pack(side="left")

        row2 = tk.Frame(main_column)
        row2.pack(fill="x")
        tk.Label(row2, text="Ending Range").pack(side="left")
        self.range_end_entry = tk.Entry(row2, width=10)
        self.range_end_entry.insert(0, str(defaults["range_end"]))
        self.range_end_entry.pack(side="left")

        rowEpoch = tk.Frame(main_column)
        rowEpoch.pack(fill="x")
        tk.Label(rowEpoch, text="Epochs").pack(side="left")
        self.epochs_entry = tk.Entry(rowEpoch, width=10)
        self.epochs_entry.insert(0, str(defaults["epochs"]))
        self.epochs_entry.pack(side="left")

        row3 = tk.Frame(main_column)
        row3.pack(fill="x")
        tk.Label(row3, text="Population Amount").pack(side="left")
        self.population_amount_entry = tk.Entry(row3, width=10)
        self.population_amount_entry.insert(0, str(defaults["population_size"]))
        self.population_amount_entry.pack(side="left")

        row4 = tk.Frame(main_column)
        row4.pack(fill="x")
        tk.Label(row4, text="Precision").pack(side="left")
        self.precision_entry = tk.Entry(row4, width=10)
        self.precision_entry.insert(0, str(defaults["precision"]))
        self.precision_entry.pack(side="left")

        row5 = tk.Frame(main_column)
        row5.pack(fill="x")
        tk.Label(row5, text="Num of Variables").pack(side="left")
        self.variables_num_entry = tk.Entry(row5, width=10)
        self.variables_num_entry.insert(0, str(defaults["num_variables"]))
        self.variables_num_entry.pack(side="left")

        row6 = tk.Frame(main_column)
        row6.pack(fill="x")
        tk.Label(row6, text="Selection Method").pack(side="left")
        self.select_method_var = tk.StringVar()
        self.select_method_combo = ttk.Combobox(row6, textvariable=self.select_method_var)
        self.select_method_combo['values'] = self.selection_methods
        self.select_method_combo.set(defaults["selection_method"])
        self.select_method_combo.pack(side="left")

        row7 = tk.Frame(main_column)
        row7.pack(fill="x")
        tk.Label(row7, text="Select best amount").pack(side="left")
        self.best_amount_entry = tk.Entry(row7, width=10)
        self.best_amount_entry.insert(0, str(defaults["best_selection_amount"]))
        self.best_amount_entry.pack(side="left")

        row8 = tk.Frame(main_column)
        row8.pack(fill="x")
        tk.Label(row8, text="Selection size").pack(side="left")
        self.selection_size_entry = tk.Entry(row8, width=10)
        self.selection_size_entry.insert(0, str(defaults["tournament_size"]))
        self.selection_size_entry.pack(side="left")

        row9 = tk.Frame(main_column)
        row9.pack(fill="x")
        tk.Label(row9, text="Cross Method").pack(side="left")
        self.cross_method_var = tk.StringVar()
        self.cross_method_combo = ttk.Combobox(row9, textvariable=self.cross_method_var)
        self.cross_method_combo['values'] = self.cross_methods
        self.cross_method_combo.set(defaults["crossover_method"])
        self.cross_method_combo.pack(side="left")

        row10 = tk.Frame(main_column)
        row10.pack(fill="x")
        tk.Label(row10, text="Cross Propability").pack(side="left")
        self.cross_propability_entry = tk.Entry(row10, width=10)
        self.cross_propability_entry.insert(0, str(defaults["crossover_probability"]))
        self.cross_propability_entry.pack(side="left")

        row11 = tk.Frame(main_column)
        row11.pack(fill="x")
        tk.Label(row11, text="Mutation Method").pack(side="left")
        self.mutation_method_var = tk.StringVar()
        self.mutation_method_combo = ttk.Combobox(row11, textvariable=self.mutation_method_var)
        self.mutation_method_combo['values'] = self.mutation_methods
        self.mutation_method_combo.set(defaults["mutation_method"])
        self.mutation_method_combo.pack(side="left")

        row12 = tk.Frame(main_column)
        row12.pack(fill="x")
        tk.Label(row12, text="Mutation Propability").pack(side="left")
        self.mutation_propability_entry = tk.Entry(row12, width=10)
        self.mutation_propability_entry.insert(0, str(defaults["mutation_probability"]))
        self.mutation_propability_entry.pack(side="left")

        row13 = tk.Frame(main_column)
        row13.pack(fill="x")
        tk.Label(row13, text="Inversion Probability").pack(side="left")
        self.inversion_propability_entry = tk.Entry(row13, width=10)
        self.inversion_propability_entry.insert(0, str(defaults["inversion_probability"]))
        self.inversion_propability_entry.pack(side="left")

        row14 = tk.Frame(main_column)
        row14.pack(fill="x")
        tk.Label(row14, text="Maximization").pack(side="left")
        self.maximization_var = tk.BooleanVar(value=defaults["optimization_type"] == "max")
        self.maximization_checkbox = tk.Checkbutton(row14, variable=self.maximization_var)
        self.maximization_checkbox.pack(side="left")


        self.start_button = tk.Button(main_column, text="Start", command=self.run_algorithm)
        self.start_button.pack(fill="x")


    def save_results_to_file(self, results):
        folder = "results"
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, "wyniki.txt")
        try:
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(results + "\n" + "="*50 + "\n")
            print(f"Wyniki dopisano do: {file_path}")
        except Exception as e:
            print(f"Błąd podczas zapisu: {str(e)}")


    def run_algorithm(self):
        try:
            from algorithms.config import config
            
            config.range_start = float(self.range_start_entry.get())
            config.range_end = float(self.range_end_entry.get())
            config.epochs = int(self.epochs_entry.get())
            config.population_size = int(self.population_amount_entry.get())
            config.precision = int(self.precision_entry.get())
            config.num_variables = int(self.variables_num_entry.get())
            config.selection_method = self.select_method_var.get().lower()
            config.best_selection_amount = int(self.best_amount_entry.get())
            config.tournament_size = int(self.selection_size_entry.get())
            config.crossover_method = self.cross_method_var.get().replace("-", "_").lower()
            config.crossover_probability = float(self.cross_propability_entry.get())
            config.mutation_method = self.mutation_method_var.get().lower()
            config.mutation_probability = float(self.mutation_propability_entry.get())
            config.inversion_probability = float(self.inversion_propability_entry.get())
            config.optimization_type = "max" if self.maximization_var.get() else "min"
            
            best_solution, execution_time, plotter = run_genetic_algorithm()
            
            results = f"Najlepsze rozwiązanie: {best_solution.chromosome_values}\nWartość funkcji celu: {best_solution.fitness}\nCzas wykonania: {execution_time} sekund\n"

            self.save_results_to_file(results)
            
            
        except Exception as e:
            print(f"Błąd: {str(e)}")
            import traceback
            traceback.print_exc()