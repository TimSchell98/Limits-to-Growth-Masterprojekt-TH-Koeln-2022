'''
Hier soll die CSV-Datei mit allen Daten aus der Wolfram Version eingelesen und bearbeitet werden
'''

# - - - - - IMPORTS - - - - - - -
import pandas as pd

#  - - - - - Funktionsdefinitionen - - - - -
def read_wolfram_export_file(path_to_csv_file):
    data = pd.read_csv(path_to_csv_file)

    print(data)


if __name__ == '__main__':
    wolfram_standard_run_csv_file = 'data/standard_run_world3_3_wolfram.csv'
    read_wolfram_export_file(wolfram_standard_run_csv_file)
    print('Data_Comparison.py')