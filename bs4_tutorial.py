import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


url = 'https://tululu.org/b9/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
book_name = soup.find('div', id='content').find('h1')
book_name_list = book_name.text.split('::')
# print(book_name_list[0].strip())
# print(book_name_list[1].strip())
# for i in soup.find_all('div', class_='texts'):
#     print(i.find('span').text)
book_genre = soup.find('div', id='content').find('span', class_='d_book')
print(book_genre.text)
# image_tag = soup.find('div', class_='bookimage').find('img')['src']
# print(urljoin('https://tululu.org/',image_tag))
# text_tag = soup.find('div', class_='entry-content')
# print(text_tag.text)