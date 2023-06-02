import json

from classes.vacancy_class import Vacancy


class JSONSaver:
    """
    Класс для сохранения данных о вакансиях в json файл, получения вакансий оттуда и удаления
    """

    def __init__(self, keyword: str):
        """
        Инициализатор класса

        :param keyword: имя для файла
        """

        self.__filename = f'{keyword.title()}.json'  # имя файла

    @property
    def filename(self):
        return self.__filename

    def add_vacancies(self, hh_vacancies: list | None = None, sj_vacancies: list | None = None) -> None:
        """
        Записывает список с вакансиями в json файлы (вакансии hh в один файл, sj в другой файл)
        """

        with open(f'hh_{self.__filename}', 'w', encoding='UTF-8') as hh_file, \
                open(f'sj_{self.__filename}', 'w', encoding='UTF-8') as sj_file:
            json.dump(hh_vacancies, hh_file, indent=4, ensure_ascii=False)
            json.dump(sj_vacancies, sj_file, indent=4, ensure_ascii=False)

    def select(self) -> list[Vacancy]:
        """
        Функция для чтения json файла с вакансиями и создания из него списка с экземплярами класса Vacancy
        """

        with open(f'hh_{self.__filename}', 'r', encoding='UTF-8') as hh_file, \
                open(f'sj_{self.__filename}', 'r', encoding='UTF-8') as sj_file:
            hh_data = json.load(hh_file)
            sj_data = json.load(sj_file)

            vacancies = []
            if hh_data:
                for vacancy in hh_data:
                    salary_min = vacancy['salary']['from'] if vacancy['salary']['from'] else vacancy['salary']['to']
                    salary_max = vacancy['salary']['to'] if vacancy['salary']['to'] else salary_min
                    requirement = vacancy['snippet']['requirement'] if vacancy['snippet']['requirement'] \
                        else 'Нет требований'
                    responsibility = vacancy['snippet']['responsibility'] if vacancy['snippet']['responsibility'] \
                        else 'Нет описания'

                    vacancies.append(Vacancy(vacancy['name'],
                                             salary_min,
                                             salary_max,
                                             vacancy['alternate_url'],
                                             vacancy['salary']['currency'],
                                             vacancy['area']['name'],
                                             requirement,
                                             responsibility,
                                             vacancy['experience']['name']))

            if sj_data:
                for vacancy in sj_data:
                    responsibility = vacancy['work'] if vacancy['work'] else 'Нет описания'
                    requirement = vacancy['candidat'] if vacancy['candidat'] else 'Нет требований'
                    vacancies.append(Vacancy(vacancy['profession'],
                                             vacancy['payment_from'],
                                             vacancy['payment_to'],
                                             vacancy['link'],
                                             vacancy['currency'],
                                             vacancy['town']['title'],
                                             requirement,
                                             responsibility,
                                             vacancy['experience']['title']))

            return vacancies

    @staticmethod
    def get_vacancies_by_salary(salary: str, vacancies: list[Vacancy]) -> list[Vacancy]:
        """
        Фильтрация вакансий по зарплате

        :param vacancies: список с экземплярами класса Vacancy
        :param salary: параметры фильтрации в следующем формате: минимальная з/п-максимальная з/п. Можно указать одно
        значение з/п, оно будет считаться минимальным, в фильтр попадут все вакансии с з/п больше либо равной переданной
        :return: отфильтрованный список вакансий
        """

        if '-' in salary:
            user_filter = salary.split('-')
            user_min, user_max = user_filter[0], user_filter[1]
            if not user_min.isdigit() and not user_max.isdigit():
                raise ValueError('Введите корректный фильтр по зарплате')
            filtered_vacancies = filter(lambda x: int(user_min) <= x.salary_min <= int(user_max), vacancies)

        else:
            user_min = salary
            if not user_min.isdigit():
                raise ValueError('Введите корректный фильтр по зарплате')
            filtered_vacancies = filter(lambda x: int(user_min) <= x, vacancies)

        return list(filtered_vacancies)

    @staticmethod
    def get_vacancies_by_region(region: str, vacancies: list[Vacancy]) -> list[Vacancy]:
        """
        Фильтрация вакансий по региону

        :param vacancies: список с экземплярами класса Vacancy
        :param region: регион
        :return: список с экземплярами класса Vacancy у которых в атрибуте area есть переданный регион
        """

        filtered_vacancies = filter(lambda x: region.lower() in x.area.lower(), vacancies)

        return list(filtered_vacancies)

    def save_results_to_json(self, vacancies: list[Vacancy]) -> None:
        """
        Запись отфильтрованных и отсортированных результатов в отдельный json файл

        :param vacancies: Список экземпляров класса Vacancy
        :return:
        """

        result = [vacancy.__dict__ for vacancy in vacancies]
        with open(f'result_{self.__filename}', 'w', encoding='UTF-8') as result_file:
            json.dump(result, result_file, indent=4, ensure_ascii=False)

    @staticmethod
    def delete_vacancy(vac_id: int, vacancies: list[Vacancy]):
        """
        Удаление из списка экземпляра класса Vacancy по его ID

        :param vac_id: id вакансии
        :param vacancies: список экземпляров класса Vacancy
        :return: None
        """

        for vacancy in vacancies:
            if vacancy.id == vac_id:
                vacancies.remove(vacancy)
                break
        print('Не найдено вакансий по переданному id')
