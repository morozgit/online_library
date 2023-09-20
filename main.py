import requests
import os
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError('HTTP Error')


def download_txt(url, filename, folder='Books/'):
    response = requests.get(url)
    response.raise_for_status()
    path_to_file = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    with open(path_to_file, 'wb') as file:
        file.write(response.content)
    return path_to_file


def main():

    path = './Books'
    os.makedirs(path, exist_ok=True)
    for i in range(1, 11):
        url = f'https://tululu.org/b{i}/'
        book_url = f'https://tululu.org/txt.php?id={i}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            book_name = soup.find('div', id='content').find('h1')
            book_name_list = book_name.text.split('::')
            filename = f'{i}. {book_name_list[0].strip()}'
            download_txt(book_url, filename, folder='Books/')
            
        except requests.HTTPError as err:
            print(err.args[0])


if __name__ == '__main__':
    main()
