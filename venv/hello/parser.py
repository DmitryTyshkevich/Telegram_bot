import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import json



async def get_page_data(session, url_):
    '''Функция собирает данные со страницы'''
    headers = {
        'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9,image/webp, */*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/112.0.0.0 Safari/537.36'
    }
    async with session.get(url=url_, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'html.parser')
        model = soup.find_all('h3', 'listing-item__title')
        key = url_.split('/')
        links_per_model[f'{key[-2]}_{key[-1]}'.upper()] = []
        for link in model:
            l = link.a.attrs.get('href')
            links_per_model[f'{key[-2]}_{key[-1]}'.upper()].append('https://cars.av.by' + l)


async def gather_data():
    '''Функция формирует список ссылок на модели Audi ckass A и список задач'''

    async with ClientSession() as session:
        headers = {
            'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9,image/webp, */*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/112.0.0.0 Safari/537.36'
        }
        async with session.get(url='https://cars.av.by/audi', headers=headers) as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'html.parser')
            models = soup.find_all('li', 'catalog__item')

            for link in models:
                if 'A' in link.text:
                    model_links.append('https://cars.av.by' + link.a.attrs.get('href'))
        tasks = []
        for url in model_links:
            task = asyncio.create_task(get_page_data(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)


def parser_run():
    asyncio.run(gather_data())
    # with open('data.json', 'w', encoding='utf-8') as file:
    #     json.dump(links_per_model, file, indent=4, ensure_ascii=False)


model_links = []
links_per_model = {}

parser_run()

