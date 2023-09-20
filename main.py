import requests
import os
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse, urlsplit


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


def download_image(url, folder='images/'):
    url_image = urljoin('https://tululu.org/', url)
    response = requests.get(url_image)
    response.raise_for_status()
    file_name = urlsplit(url_image).path.split('/')[-1]
    image_path = os.path.join(folder, file_name)
    with open(image_path, 'wb') as file:
        file.write(response.content)


def main():

    path_book = './Books'
    os.makedirs(path_book, exist_ok=True)
    path_image = './images'
    os.makedirs(path_image, exist_ok=True)
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
            # download_txt(book_url, filename, folder='Books/')
            image_tag = soup.find('div', class_='bookimage').find('img')['src']
            download_image(image_tag)
        except requests.HTTPError as err:
            print(err.args[0])


if __name__ == '__main__':
    main()
