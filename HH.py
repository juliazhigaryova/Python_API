from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import requests
import re
from pprint import pprint

# реализация получения вакансий c сайта hh.ru и сохранения в базу.

text = input("Введите название вакансии: ")
pages = int(input("Введите количество страниц сайта: "))


def get_save_vacancies_hh(text, pages):
    client = MongoClient('127.0.0.1', 27017)
    db = client['vacancies']
    vacancies_hh = db.vacancies_hh

    main_link = 'https://hh.ru'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    page = 0
    vacancies = []
    for i in range(page, pages):
        response = requests.get(
            main_link + '/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=' + text + '&page=' + str(i),
            headers=headers)
        soup = bs(response.text, 'html.parser')
        vacancies_list = soup.find_all('div', {'class': 'vacancy-serp-item'})
        for vacancy in vacancies_list:
            vacancy_data = {}
            vacancy_link = vacancy.find('a', class_='bloko-link HH-LinkModifier').get('href')
            vacancy_name = vacancy.find('a', class_='bloko-link HH-LinkModifier').getText()
            try:
                salary = vacancy.find('span', {"data-qa": "vacancy-serp__vacancy-compensation"}).getText()
                if salary.startswith('от'):
                    if salary.endswith('USD'):
                        vacancy_salary_min = int(re.sub(r'[^0-9]+', r'', salary))
                        vacancy_salary_max = 'None'
                        vacancy_cur = 'USD'
                    else:
                        vacancy_salary_min = int(re.sub(r'[^0-9]+', r'', salary))
                        vacancy_salary_max = 0
                        vacancy_salary_cur = 'руб.'
                elif salary.startswith('до'):
                    if salary.endswith('USD'):
                        vacancy_salary_min = 0
                        vacancy_salary_max = int(re.sub(r'[^0-9]+', r'', salary))
                        vacancy_cur = 'USD'
                    else:
                        vacancy_salary_min = 0
                        vacancy_salary_max = int(re.sub(r'[^0-9]+', r'', salary))
                        vacancy_salary_cur = 'руб.'
                elif len(salary) == 0:
                    vacancy_salary_min = 0
                    vacancy_salary_max = 0
                    vacancy_salary_cur = 0
                else:
                    if salary.endswith('USD'):
                        vacancy_salary_pre = re.sub(r'[^0-9-]+', r'', salary)
                        vacancy_salary_pre = vacancy_salary_pre.split('-')
                        vacancy_salary_min = int(vacancy_salary_pre[0])
                        vacancy_salary_max = int(vacancy_salary_pre[1])
                        vacancy_salary_cur = 'USD'
                    else:
                        vacancy_salary_pre = re.sub(r'[^0-9-]+', r'', salary)
                        vacancy_salary_pre = vacancy_salary_pre.split('-')
                        vacancy_salary_min = int(vacancy_salary_pre[0])
                        vacancy_salary_max = int(vacancy_salary_pre[1])
                        vacancy_salary_cur = 'руб.'
            except:
                vacancy_salary_min = 0
                vacancy_salary_max = 0
                vacancy_salary_cur = 0
            vacancy_site = main_link
            vacancy_data['name'] = vacancy_name
            vacancy_data['link'] = vacancy_link
            vacancy_data['salary_min'] = vacancy_salary_min
            vacancy_data['salary_max'] = vacancy_salary_max
            vacancy_data['salary_cur'] = vacancy_salary_cur
            vacancy_data['site'] = vacancy_site

            # проверка на дубликаты
            duplicates = vacancies_hh.find_one({'$or': [{'link': vacancy_link}, {'salary_min': vacancy_salary_min},
                                               {'salary_max': vacancy_salary_max}]})
            if duplicates is None:
                vacancies_hh.insert_one(vacancy_data)
            else:
                pass

            vacancies.append(vacancy_data)
            if not soup.find('a', attrs={'data-qa': 'pager-next'}):
                break

    return pprint(vacancies)


get_save_vacancies_hh(text, pages)
