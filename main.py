import requests
from bs4 import BeautifulSoup
import time
import telebot


TELEGRAM_TOKEN = ''  # enter token
CHAT_ID = ''  # enter id

bot = telebot.TeleBot(TELEGRAM_TOKEN)

#URL = 'https://djinni.co/jobs/?all-keywords=&any-of-keywords=&exclude-keywords=&primary_keyword=QA&primary_keyword=QA+Automation&exp_level=no_exp&exp_level=1y'
URL = "https://djinni.co/jobs/"

SENT_VACANCIES_FILE = 'sent_vacancies.txt'


def load_sent_vacancies():
    try:
        with open(SENT_VACANCIES_FILE, 'r') as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()


def save_sent_vacancies(sent_vacancies):
    with open(SENT_VACANCIES_FILE, 'w') as file:
        file.write('\n'.join(sent_vacancies))


def check_for_new_vacancies():
    sent_vacancies = load_sent_vacancies()

    while True:
        try:
            response = requests.get(URL)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            vacancies = soup.find_all('li', class_='list-jobs__item')

            for vacancy in vacancies:
                vacancy_title = vacancy.find('div', class_='list-jobs__title').text.strip()
                vacancy_link = vacancy.find('a', class_='profile').get('href')
                vacancy_info = f"vacancy: {vacancy_title}\nLink: https://djinni.co{vacancy_link}\n"


                if ('Automation' in vacancy_title or 'qa' in vacancy_title or 'QA' in vacancy_title) and vacancy_info not in sent_vacancies:
                    bot.send_message(CHAT_ID, vacancy_info)
                    sent_vacancies.add(vacancy_info)
            save_sent_vacancies(sent_vacancies)

        except Exception as e:
            print(f"Error occurred: {e}")

        time.sleep(15)


if __name__ == '__main__':
    check_for_new_vacancies()
