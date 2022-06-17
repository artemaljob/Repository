# Сохранить "Главную страницу" с полным html содержимым.
import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# URL = 'https://volgograd.hh.ru/search/vacancy?area=24'
URL = 'https://volgograd.hh.ru/vacancies/programmist'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.60',
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
HOST = 'https://volgograd.hh.ru'
FILE = 'jobs.csv'

# get_html и get_pages_count нужны только что бы получить кол-во страниц с вакансиями.
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='pager-item-not-in-short-range')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1

# Решение следующее:
# - записываю контент страницы через Selenium
# - в следующей программе паршу его BeautifulSoup'ом

def get_content():
    # Получить номер последней страницы.
    html = get_html(URL)
    pages_count = get_pages_count(html.text)
    print(f'Кол-во страниц с вакансиями {pages_count}')

    # настройка options для Chrome и FireFox https://stackoverflow.com/questions/29916054/change-user-agent-for-selenium-web-driver
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.60")

    try:
        for i in range (1, pages_count + 1):
            url = f'https://volgograd.hh.ru/vacancies/programmist?page={i-1}'
            driver = webdriver.Chrome(
                executable_path="H:\Job\Parser\Парсер hhRu\Selenium Parser\hhRu (page downloader)\chromedriver.exe",
                chrome_options=options
            )
            driver.get(url=url)
            time.sleep(random.randrange(2, 5))

            with open(f"html\hhRu_{i}.html", "w", encoding="UTF-8") as file:
                file.write(driver.page_source)
        return pages_count + 1
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

get_content()
