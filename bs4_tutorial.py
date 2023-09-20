import requests
from bs4 import BeautifulSoup


url = 'https://tululu.org/b1/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
book_name = soup.find('div', id='content').find('h1')
book_name_list = book_name.text.split('::')
print(book_name_list[0].strip())
print(book_name_list[1].strip())
# title_text = title_tag.text
# print(title_text)
# image_tag = soup.find('img', class_='attachment-post-image')['src']
# print(image_tag)
# text_tag = soup.find('div', class_='entry-content')
# print(text_tag.text)