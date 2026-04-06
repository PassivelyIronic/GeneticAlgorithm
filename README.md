# Algorytm Genetyczny

Prosta aplikacja w języku Python wyposażona w interfejs graficzny do uruchamiania i analizy algorytmów genetycznych. Projekt pozwala na elastyczne testowanie różnych parametrów i operatorów ewolucyjnych.

## Funkcje
* **Interfejs graficzny (GUI):** Zbudowany przy użyciu biblioteki Tkinter, pozwala na zdefiniowanie parametrów takich jak liczba epok, wielkość populacji, szansa na krzyżowanie czy mutację.
* **Metody selekcji:** Do wyboru selekcja najlepszych osobników (Best), ruletkowa (Roulette) oraz turniejowa (Tournament).
* **Metody krzyżowania:** Jednopunktowe (Single-point), dwupunktowe (Two-point) i równomierne (Uniform).
* **Metody mutacji:** Jednopunktowa, dwupunktowa oraz brzegowa (Edge).
* **Wizualizacje:** Aplikacja korzysta z biblioteki Matplotlib do generowania wykresów z historią przystosowania, zbieżnością algorytmu oraz wizualizacjami 3D powierzchni funkcji celu.
* **Zapis wyników:** Automatyczny zapis najlepszych rozwiązań oraz czasu wykonania, a także eksport wykresów.

## Wymagania

Aby uruchomić projekt, upewnij się, że masz zainstalowanego Pythona (wersja 3.x). Wymagane są również dodatkowe biblioteki, które zainstalujesz poleceniem:

```bash
pip install numpy matplotlib

python -m apps.main
