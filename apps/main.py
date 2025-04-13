import tkinter as tk
from apps.views import MainWindow
from algorithms.genetic import run_genetic_algorithm

def main():
    app = MainWindow()
    app.root.mainloop()
    

if __name__ == "__main__":
    main()