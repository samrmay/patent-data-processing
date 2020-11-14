# Script to process zip files into csv/ format AI can handle
import zipfile
import xml
import os
import re
import xml.etree.ElementTree as ET
import csv

DATA_DIR = 'data'
OUTPUT_DIR = 'output'
# Data structure should follow a parent_dir/year/data.zip/file.xml format


def open_zips(data_dir):
    year_dirs = os.listdir(data_dir)
    try:
        os.mkdir(f'{OUTPUT_DIR}')
    except FileExistsError:
        pass
    for year in year_dirs:
        year_dir = f'{data_dir}/{year}'
        zips_arr = os.listdir(year_dir)
        if len(zips_arr) > 0:
            try:
                os.mkdir(f'{OUTPUT_DIR}/{year}')
            except FileExistsError:
                pass
            for item in zips_arr:
                zip_path = f'{year_dir}/{item}'
                try:
                    with zipfile.ZipFile(zip_path) as myzip:
                        zip_contents = myzip.infolist()
                        if len(zip_contents) > 0 and not zip_contents[0].is_dir():
                            data_file_name = zip_contents[0].filename
                            with myzip.open(data_file_name) as data_file:
                                if re.match(r"^.*\.(xml)$", data_file_name):
                                    save_xml(
                                        data_file, f'{OUTPUT_DIR}/{year}/{data_file_name[:-4]}')
                                elif re.match(r"^.*\.(aps)$", data_file_name):
                                    save_aps(data_file)
                                elif re.match(r"^.*\.(patft)$", data_file_name):
                                    save_patft(data_file)
                except zipfile.BadZipFile:
                    print(f'Error: could not open {zip_path}')


def save_xml(file, output):
    working_xml = ''
    xml_index = 0
    with open(output + '.csv', 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['description'])
    for line in file:
        line = line.decode('utf-8')
        if '<?xml version="1.0" encoding="UTF-8"?>' in line:
            if xml_index > 0:
                with open(output + '.csv', 'a', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    root = ET.fromstring(working_xml)
                    content_to_write = ''
                    for child in root:
                        if child.tag == 'abstract':
                            for child2 in child:
                                if type(child2.text) == str:
                                    content_to_write += child2.text
                                try:
                                    for child3 in child2:
                                        content_to_write += child3.text
                                        content_to_write += child3.tail
                                except TypeError:
                                    pass
                            if len(content_to_write) > 0:
                                formatted_content = content_to_write.replace(
                                    ',', ' ')
                                writer.writerow([formatted_content])
            xml_index += 1
            working_xml = line
            print(f'{xml_index} patents processed for {output}', end='\r')
        else:
            working_xml += line
    print(f'Saved {output} after processing {xml_index} patents')


def save_aps(file):
    print(file.read())


def save_patft(file):
    print(file.read())


open_zips(DATA_DIR)
