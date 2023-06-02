from classes import hh_sj_classes
from classes.hh_sj_classes import HeadHunterAPI, SuperJobAPI
from classes.json_saver_class import JSONSaver
from classes.vacancy_class import Vacancy


def sort_vacancies(vacancies: list[Vacancy]) -> list[Vacancy]:
    """
    Функция для сортировки списка вакансий по зарплате

    :param vacancies: список с экземплярами класса Vacancy
    :return: отсортированный по минимальной зарплате список с экземплярами класса Vacancy
    """

    sorted_vacancies = sorted(vacancies)

    return sorted_vacancies


def filter_vacancies(filter_word: str, vacancies: list[Vacancy]) -> list[Vacancy]:
    """
    Поиск вакансий по ключевому слову. Ключевое слово ищется в описании вакансии, или в требованиях к вакансии

    :param filter_word: ключевое слово
    :param vacancies: список с экземплярами класса Vacancy
    :return: список с экземплярами класса Vacancy, в описании у которых найдено ключевое слово
    """

    filtered_vac = []
    for vacancy in vacancies:
        if filter_word.lower() in vacancy.requirement.lower() or filter_word.lower() in vacancy.responsibility.lower():
            filtered_vac.append(vacancy)

    return filtered_vac


def get_top_vacancies(vacancies: list[Vacancy], top_n: int) -> list[Vacancy]:
    """
    Функция для возврата top_n вакансий с самой большой зарплатой

    :param vacancies: отсортированный по возрастанию з/п список с экземплярами класса Vacancy
    :param top_n: количество вакансий для вывода
    :return: список с top_n экземплярами класса Vacancy с самой большой зарплатой
    """

    return vacancies[-1:-top_n:-1]


def get_vacancies_without_experience(vacancies: list[Vacancy]):
    filtered_vacancies = filter(lambda x: x.experience == 'Нет опыта' or
                                          x.experience == 'без опыта' or
                                          '1' in x.experience,
                                vacancies)

    return list(filtered_vacancies)


def print_vacancies(vacancies: list[Vacancy]) -> None:
    """
    Функция для вывода в консоль списка вакансий
    """

    print(*vacancies, sep='\n++++++++++++++++++++++++++++++++++++++\n')


def choose_platform(keyword: str) -> tuple:
    """
    Функция для выбора платформы для парсинга

    :param keyword: ключевое слово (hh для Headhunter, sj для Superjob)
    :return: созданные в соответствии с ключевым словом экземпляры классов HH и SJ
    """

    # начальные значения для платформ
    hh_api = None
    sj_api = None

    # Если пользователь ввел hh или HH, создается экземпляр класса HeadHunterAPI()
    if keyword.lower() == 'hh':
        hh_api = hh_sj_classes.HeadHunterAPI()

    # Если пользователь ввел sj или SJ, создается экземпляр класса SuperJobAPI()
    elif keyword.lower() == 'sj':
        sj_api = hh_sj_classes.SuperJobAPI()

    # Во всех остальных случаях создается два экземпляра класса: HeadHunterAPI() и SuperJobAPI()
    else:
        hh_api = hh_sj_classes.HeadHunterAPI()
        sj_api = hh_sj_classes.SuperJobAPI()

    return hh_api, sj_api


def parse(api_hh: None | HeadHunterAPI, api_sj: None | SuperJobAPI, keyword: str, count: str) -> tuple:
    """
    Функция для отправки запросов на api

    :param api_hh: Экземпляр класса HeadHunterAPI или None
    :param api_sj: Экземпляр класс SuperJobAPI или None
    :param keyword: Ключевое слово, по которому будут искаться вакансии
    :param count: Количество страниц с вакансиями (1 страница - 100 вакансий)
    :return: список с экземплярами классов Vacancy для HeadHunterAPI и SuperJobAPI
    """

    # если есть экземпляр класса HeadHunterAPI() и нет экземпляра класса SuperJobAPI()
    if api_hh is None:
        hh_vacancies = None  # Вакансии с сайта hh
        sj_vacancies = api_sj.get_vacancies(keyword, count)

        # если есть экземпляр класса SuperJobAPI() и нет экземпляра класса HeadHunterAPI()
    elif api_sj is None:
        sj_vacancies = None  # вакансии с сайта sj
        hh_vacancies = api_hh.get_vacancies(keyword, count)  # Вакансии с сайта hh

        # во всех остальных случаях должны создаться два экземпляра: HeadHunterAPI() и SuperJobAPI()
    else:
        hh_vacancies = api_hh.get_vacancies(keyword, count)  # Вакансии с сайта hh
        sj_vacancies = api_sj.get_vacancies(keyword, count)  # вакансии с сайта sj

    return hh_vacancies, sj_vacancies


def user_filter(query, vacancies) -> list[Vacancy]:
    """
    Функция для выбора каким образом отфильтровать вакансии

    :param query: Ключ фильтрации
    :param vacancies: список с экземплярами классов Vacancy
    :return: отфильтрованный список с экземплярами классов Vacancy
    """

    # Фильтрация по зарплате
    if query == '1':
        salary = input('Введите желаемый уровень оклада в рублях, например 40000-60000, или 80000 -> ')
        vacancies = JSONSaver.get_vacancies_by_salary(salary, vacancies)

    # Фильтрация по региону
    elif query == '2':
        region = input('Введите регион -> ')
        vacancies = JSONSaver.get_vacancies_by_region(region, vacancies)

    # Фильтрация по опыту работы
    elif query == '3':
        vacancies = get_vacancies_without_experience(vacancies)

    return vacancies
