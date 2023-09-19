import requests
import os


def main():
    path = './Books'
    os.makedirs(path, exist_ok=True)
    print(path)
    for i in range(1, 11):
        url = f'https://tululu.org/txt.php?id={i}'
        response = requests.get(url)
        response.raise_for_status()
        filename = f'id{i}.txt'
        with open(os.path.join(path, filename), 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    main()
