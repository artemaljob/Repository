from bs4 import BeautifulSoup
import csv

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.60'}
HOST = 'https://volgograd.hh.ru'

def parse():
    pages_count = 40
    jobs = []
    for i in range (1, pages_count + 1):

        with open(f'H:\Job\Parser\Парсер hhRu\Selenium Parser\hhRu (page downloader)\html\hhRu_{i}.html', encoding='UTF-8') as page_to_parse:
            src = page_to_parse.read()

            soup = BeautifulSoup(src, 'html.parser')
            items = soup.find_all('div', class_='vacancy-serp-item')

            for soup in items:

                try:
                    title = soup.find('a', class_='bloko-link').get_text(strip=True)
                except Exception as _ex:
                    title = None
                # print(f'{title}')

                try:
                    link = soup.find('a', class_='bloko-link').get('href')
                except Exception as _ex:
                    link = None

                try:
                    cost = soup.find('span', {"class": "bloko-header-section-3", "data-qa": "vacancy-serp__vacancy-compensation"}).get_text(strip=True).replace('\xa0', ' ').replace('от ', '').replace('от', '').replace('до ', '').replace('до', '').replace('руб.', '')
                except Exception as _ex:
                    cost = None
                # print(f'{cost}')

                try:
                    company = soup.find('a', {"class": "bloko-link", "data-qa": "vacancy-serp__vacancy-employer"}).get_text(strip=True)
                except Exception as _ex:
                    company = None
                # print(f'{company}')

                try:
                    location = soup.find('div', {"class": "bloko-text", "data-qa": "vacancy-serp__vacancy-address"}).get_text(strip=True).replace(f'{company}', '').replace('Можно работать из дома', '')
                except Exception as _ex:
                    location = None
                # print(location)

                try:
                    companylink = HOST + soup.find('a', {"class": "bloko-link", "data-qa": "vacancy-serp__vacancy-employer"}).get('href')
                except Exception as _ex:
                    companylink = None
                # print(companylink)

                jobs.append({
                    'title': title,
                    'link': link,
                    'cost': cost,
                    'company': company,
                    'location': location,
                    'companylink': companylink,
                    # 'companylink': HOST + companylink,
                })


                with open('jobs.csv', 'w', newline='', encoding="utf-8-sig") as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(['Вакансия', 'Ссылка Вакансия', 'Ставка', 'Кампания', 'Оффис', 'Ссылка Кампания'])
                    for job in jobs:
                        writer.writerow([job['title'], job['link'], job['cost'], job['company'], job['location'], job['companylink']])
        print(f'{i} page is done!')


    return pages_count + 1


parse()