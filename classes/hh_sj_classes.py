import json
from abc import ABC, abstractmethod

import requests


class Engine(ABC):
    """
    Абстрактный класс-родитель для классов HH и SJ
    """

    @abstractmethod
    def get_request(self, *args, **kwargs):
        pass


class HeadHunterAPI(Engine):
    """
    Класс для работы с API сайта headhunter.ru
    """

    URL = 'https://api.hh.ru/vacancies'

    @staticmethod
    def get_region_id(region, town=None) -> str:
        """
        Получение ID региона по его названию

        :param region: название региона
        :param town: название города
        :return: id региона и id города
        """
        regions_response = requests.get('https://api.hh.ru/areas')
        for r in regions_response.json()[0]['areas']:
            if region.capitalize() in r['name']:

                # если задан город
                if town:
                    for t in r['areas']:
                        if region.capitalize() in t['name']:
                            return f"id области {region} - {r['id']}; id города {town} - {t['id']}"
                else:
                    return f"id региона {region} - {r['id']}"
        return 'Некорректный запрос'

    def get_request(self, keyword, page, area, per_page=100):
        """
        Отправка запроса на API

        :param keyword: ключевое слово (название вакансии)
        :param page: номер страницы
        :param per_page: количество вакансий на одной странице
        :param area: ID региона из справочника
        :return: json со списком вакансий
        """

        # в параметрах задана сортировка по дате и только с указанной зарплатой в рублях по России
        params = {'text': keyword,
                  'page': page,
                  'per_page': per_page,
                  'only_with_salary': True,
                  'order_by': "publication_time",
                  'area': area,
                  'currency': 'RUR'
                  }

        response = requests.get(self.URL, params=params).json()
        return response['items']

    def get_vacancies(self, keyword: str, pages, area=113) -> list[json]:
        """
        Делает запросы, изменяя номер страницы

        :param keyword: ключевое слово (название вакансии)
        :param area: ID региона из справочника (по умолчанию 113 - Вся Россия)
            1 - Москва,
            2019 - Московская область,
            2 - Санкт-Петербург
        :param pages: количество страниц для парсинга
        :return: список с вакансиями на соответствующей странице
        """

        # Максимальное количество вакансий для парсинга - 2000
        if pages > 20:
            raise ValueError('Вы превысили максимальное число вакансий, возможных для парсинга по API')

        vacancies = []  # список с вакансиями
        for page in range(pages):
            page = self.get_request(keyword, page, area)
            vacancies.extend(page)

        return vacancies


class SuperJobAPI(Engine):
    """
    Класс для работы с сайтом superjob
    """

    # токен для работы с superjob
    SUPER_SECRET_KEY = 'v3.r.137470714.2f709c74e49a5c3452e4bc542e76452080aaa3cb' \
                       '.c191c920c6f79710ba889d27e93e9bb87bdb1533 '
    # адрес сайта
    URL = 'https://api.superjob.ru/2.0/vacancies/'

    def get_request(self, keyword, page, region_id, count=100) -> json:
        """
        Метод для отправки запроса на api superjob

        :param keyword: ключевое слово (название профессии)
        :param region_id: id региона (города или области) 1-Россия
        :param page: номер страницы
        :param count: количество вакансий на странице (100 вакансий)
        :return: список вакансий, соответствующих требованиям в формате json
        """
        params = {'keyword': keyword,
                  'с': region_id,
                  'sort_new (unixtime)': 1,
                  'page': page,
                  'count': count,
                  'no_agreement': 1}

        response = requests.get(self.URL, headers={'X-Api-App-Id': self.SUPER_SECRET_KEY},
                                params=params).json()

        return response['objects']

    def get_vacancies(self, keyword, pages, region_id=1):
        """
        Метод для организации постраничной отправки запроса

        :param keyword: ключевое слово
        :param pages: количество страниц (максимальное значение для API - 5 страниц по 100 вакансий)
        :param region_id: id региона
        :return: список вакансий, собранных с сайта superjob по ключевому слову
        """

        if pages > 5:
            pages = 5
        vacancies = []
        for page in range(pages):
            response = self.get_request(keyword, page + 1, region_id)
            vacancies.extend(response)
        return vacancies
