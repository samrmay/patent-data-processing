import csv
import os

DATA_DIR = 'output'
OUTPUT_DIR = 'csv'
OUTPUT_FILE = 'patent_abstracts_clean'
MIN_LEN = 25


def combine_csv(input_dir):
    try:
        os.mkdir(OUTPUT_DIR)
    except FileExistsError:
        print('Output dir already exists')
    output_path = f'{OUTPUT_DIR}/{OUTPUT_FILE}.csv'
    if os.path.isfile(output_path):
        print('Output file already exists')
        exit()
    years = os.listdir(DATA_DIR)
    csv_index = 0
    with open(output_path, 'w', newline='', encoding='utf-8') as output:
        writer = csv.writer(output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_ALL)
        for year in years:
            dir = f'{DATA_DIR}/{year}'
            csv_arr = os.listdir(dir)
            for item in csv_arr:
                csv_path = f'{dir}/{item}'
                with open(csv_path, 'r', newline='', encoding='utf-8') as input_file:
                    reader = csv.reader(input_file)
                    csv_index += 1
                    for row in reader:
                        if len(row) > 0 and len(row[0]) > MIN_LEN:
                            writer.writerow(row)
                print(f'Copied {csv_index} files into {output_path}', end='\r')


combine_csv(DATA_DIR)
