import requests
from bs4 import BeautifulSoup
import os

BULK_DATA_URL = 'https://bulkdata.uspto.gov/'
DATA_DIR = 'data'


def get_text_zips(db_url, parent_dir):
    r = requests.get(db_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    all_links = soup.find_all('a')
    full_text_links = []
    for link in all_links:
        href = link.get('href')
        if href and 'fulltext' in href:
            full_text_links += [href]
    for link in full_text_links:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')
        zips = []
        zip_candidates = soup.find_all('a')
        for item in zip_candidates:
            if '.zip' in item.get('href'):
                zips += [item]
        if len(zips) > 0:
            data_year = link[-4:]
            print('-'*50 + f'Downloading data from {data_year}' + '-'*50)
            save_zips(link, zips, f'{parent_dir}/{data_year}')


def save_zips(parent_link, zips, data_dir, chunk_size=10240):
    file_index = 0
    create_directory(data_dir)
    for link in zips:
        file_index += 1
        link_content = f'zip{file_index}.zip'
        if len(link.contents) > 0:
            link_content = link.contents[0]
        file_dir = f'{data_dir}/{link_content}'
        if not os.path.exists(file_dir):
            href = f"{parent_link}/{link.get('href')}"
            r = requests.get(href, stream=True)
            try:
                content_size = int(r.headers['Content-Length'])/1000000
            except KeyError:
                pass
            with open(file_dir, 'wb') as file:
                print('downloading: ' + link_content)
                chunk_index = 0
                for chunk in r.iter_content(chunk_size=chunk_size):
                    chunk_index += 1
                    if content_size > 0:
                        downloaded_content = (chunk_index*chunk_size)/1000000
                        print(f'{downloaded_content}'.ljust(8) +
                              '/' + f'{content_size}mB'.ljust(10), end='\r')
                    file.write(chunk)
        else:
            print(file_dir + ' already exists. skipping.')


def create_directory(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        print(f'directory at {path} already created')


def main(db_url, parent_dir):
    create_directory(parent_dir)
    get_text_zips(db_url, parent_dir)


main(BULK_DATA_URL, DATA_DIR)
