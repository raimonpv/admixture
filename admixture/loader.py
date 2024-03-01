import csv
import os

def check_file(data_file_name):
    if not os.path.exists(data_file_name):
        raise FileNotFoundError(f"{data_file_name} does not exist.")

def ancestry(file_path):
    check_file(file_path)

    processed_data = {}
    with open(file_path, 'r') as file:
        data = filter(lambda row: len(row) == 5 and row[-1] in ['A', 'T', 'G', 'C'], csv.reader(file, delimiter='\t'))
        processed_data = {row[0]: ''.join(row[-2:]) for row in data}

    return processed_data

def twenty_three(file_path):
    pass

def thousand_genomes():
    pass
