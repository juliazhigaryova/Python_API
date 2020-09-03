from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint

main_link = 'https://www.superjob.ru'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
text = input("Введите название вакансии: ")
count = int(input("Введите количество страниц сайта: "))
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
            rep = re.compile("[^a-zA-Zа-яА-яЁё,\d]")
            vacancy_salary = rep.sub(" ", salary)
        except:
            vacancy_salary = 0
        vacancy_site = main_link

        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = main_link + vacancy_link
        vacancy_data['salary'] = vacancy_salary
        vacancy_data['site'] = vacancy_site
        vacancies.append(vacancy_data)
pprint(vacancies)