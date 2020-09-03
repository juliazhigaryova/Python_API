from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint

# не получилось придумать как распарсить отдельно минимальную и максиальную зарплату, не хватило времени, к сожалению(

main_link = 'https://hh.ru'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
text = input("Введите название вакансии: ")
pages = int(input("Введите количество страниц сайта: "))
page = 0
vacancies = []
for i in range(page,pages):
    response = requests.get(main_link + '/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=' + text + '&page=' + str(i),headers=headers)
    soup = bs(response.text,'html.parser')
    vacancies_list = soup.find_all('div',{'class':'vacancy-serp-item'})
    for vacancy in vacancies_list:
        reg_min = '/d+[0-9]{1,9}?'
        vacancy_data={}
        vacancy_link = vacancy.find('a',class_='bloko-link HH-LinkModifier').get('href')
        vacancy_name = vacancy.find('a',class_='bloko-link HH-LinkModifier').getText()
        try:
            salary = vacancy.find('span',{"data-qa" : "vacancy-serp__vacancy-compensation"}).getText()
            rep = re.compile("[^a-zA-Zа-яА-я,\d,\-]")
            vacancy_salary = rep.sub(" ", salary)
        except:
            vacancy_salary = 0
        vacancy_site = main_link
        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['salary'] = vacancy_salary
        vacancy_data['site'] = vacancy_site

        vacancies.append(vacancy_data)

pprint(vacancies)