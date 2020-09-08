from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint
from pymongo import MongoClient

# реализация получения вакансий c сайта superjob.ru и сохранения в базу.

text = input("Введите название вакансии: ")
count = int(input("Введите количество страниц сайта: "))


def get_save_vacancies_sj(text,count):
    client = MongoClient('127.0.0.1', 27017)
    db = client['vacancies']
    vacancies_sj = db.vacancies_sj
    main_link = 'https://www.superjob.ru'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    page = 1
    pages = count+1
    vacancies = []

    for i in range(page,pages):
        response = requests.get(main_link + '/vacancy/search/?keywords=' + text + '&page' + str(i),headers=headers)
        soup = bs(response.text,'html.parser')
        vacancies_list = soup.find_all('div',{'class':'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'})
        for vacancy in vacancies_list:
            vacancy_data={}
            vacancy_link = vacancy.find('div',class_='_3mfro PlM3e _2JVkc _3LJqf').find('a').get('href')
            vacancy_name = vacancy.find('div',class_='_3mfro PlM3e _2JVkc _3LJqf').find('a').getText()
            try:
                salary = vacancy.find('span',{"class" : "_3mfro _2Wp8I PlM3e _2JVkc _2VHxz"}).getText()
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
            vacancy_data['link'] = main_link + vacancy_link
            vacancy_data['salary_min'] = vacancy_salary_min
            vacancy_data['salary_max'] = vacancy_salary_max
            vacancy_data['salary_cur'] = vacancy_salary_cur
            vacancy_data['site'] = vacancy_site

            # проверка на дубликаты
            duplicates = vacancies_sj.find_one({'$or': [{'link': vacancy_link}, {'salary_min': vacancy_salary_min},
                                               {'salary_max': vacancy_salary_max}]})
            if duplicates is None:
                vacancies_sj.insert_one(vacancy_data)
            else:
                pass

            vacancies.append(vacancy_data)
            if not soup.find('a', attrs={'class': 'f-test-button-dalshe'}):
                break

    return pprint(vacancies)


get_save_vacancies_sj(text, count)
