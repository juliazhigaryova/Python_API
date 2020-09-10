from pymongo import MongoClient

# функция поиска

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
vacancies_hh = db.vacancies_hh
vacancies_sj = db.vacancies_sj

search_param = int(input('Введите размер заработной платы: '))


def search(search_param):
    result = []
    for element in vacancies_hh.find({'$or': [{'salary_min': {'$gt': search_param}},
                                              {'salary_max': {'$gt': search_param}}]}):
        result.append(element)

    for element in vacancies_sj.find({'$or': [{'salary_min': {'$gt': search_param}},
                                              {'salary_max': {'$gt': search_param}}]}):
        result.append(element)

    return result
