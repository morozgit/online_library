import argparse
import os
from urllib.parse import urljoin, urlparse, urlsplit

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError('HTTP Error')


def download_txt(url, filename, folder='Books/'):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    path_to_file = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    with open(path_to_file, 'wb') as file:
        file.write(response.content)
    return path_to_file


def download_image(url, folder='images/'):
    url_image = urljoin('https://tululu.org/', url)
    response = requests.get(url_image)
    response.raise_for_status()
    check_for_redirect(response)
    file_name = urlsplit(url_image).path.split('/')[-1]
    image_path = os.path.join(folder, file_name)
    with open(image_path, 'wb') as file:
        file.write(response.content)


def parse_book_page(response, url):
    soup = BeautifulSoup(response.text, 'lxml')
    book_html = soup.find('div', id='content').find('h1')
    book_name_author = book_html.text.split('::')
    book_name = book_name_author[0].strip()
    book_author = book_name_author[1].strip()
    book_genre = soup.find('div', id='content').find('span', class_='d_book').find('a').text
    comments = [comment.find('span').text for comment in soup.find_all('div', class_='texts')]
    image_tag = soup.find('div', class_='bookimage').find('img')['src']
    image_url = urljoin(url, image_tag)
    book_tag = soup.find('div', id='content').find_all('a')[10]['href']
    book_url = urljoin(url, book_tag)
    book_data = {
        'book_name': book_name,
        'book_author': book_author,
        'book_genre': book_genre,
        'comments': comments,
        'image_url': image_url,
        'book_url': book_url,
    }
    return book_data


def main():

    path_book = './Books'
    os.makedirs(path_book, exist_ok=True)
    path_image = './images'
    os.makedirs(path_image, exist_ok=True)
    parser = argparse.ArgumentParser(
        description='Описание что делает программа'
    )
    parser.add_argument('-start', help='Первая книга', type=int, default=1)
    parser.add_argument('-end', help='Последня книга', type=int, default=11)
    args = parser.parse_args()

    for i in range(args.start, args.end + 1):
        url = f'https://tululu.org/b{i}/'
        try:
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            books_data = parse_book_page(response, url)
            download_txt(books_data['book_url'], f"{i}. {books_data['book_name']}")
            download_image(books_data['image_url'])
        except requests.HTTPError as err:
            print(err.args[0])


if __name__ == '__main__':
    main()
