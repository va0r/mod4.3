from utils.utils import *


def user_interaction():
    print("Курсовой проект по теме объектно-ориентированное программирование: Парсинг вакансий")
    input('======================= Нажмите Enter чтобы начать ================================\n')

    # Запрос платформ для поиска
    query = input('Введите платформы для поиска вакансий HH - Headhunter, SJ - SuperJob.'
                  'Для поиска вакансий на двух платформах нажмите Enter -> ')

    hh_api, sj_api = choose_platform(query)  # выбор платформы для парсинга

    # запрос у пользователя ключевого слова для поиска по вакансиям
    keyword = input('Введите поисковый запрос -> ')

    # Запрос у пользователя количества страниц для парсинга
    count = int(input('Введите количество страниц для парсинга (1 страница - 100 вакансий) -> '))

    hh_vacancies, sj_vacancies = parse(hh_api, sj_api, keyword, count)  # Вызов метода для парсинга

    if hh_vacancies:
        print(f'Парсинг прошел успешно. Найдено {len(hh_vacancies)} вакансий с сайта headhunter.ru')
    if sj_vacancies:
        print(f'Парсинг прошел успешно. Найдено {len(sj_vacancies)} вакансий с сайта superjob.ru')
    if not hh_vacancies and not sj_vacancies:
        print('Нет вакансий, соответствующих заданным критериям')
        exit()

    json_saver = JSONSaver(keyword)  # Создание экземпляра класса JSONSaver
    json_saver.add_vacancies(hh_vacancies, sj_vacancies)  # Добавление вакансий в json файлы (отдельно hh и sj)
    vacancies_classes = json_saver.select()  # Создание списка с экземплярами класса Vacancy

    filter_word = input("Введите ключевое слово для поиска в описании вакансий"
                        "Для пропуска данного фильтра нажмите Enter -> ")  # ключевое слово для поиска

    if filter_word:
        filtered_vacancies = filter_vacancies(filter_word, vacancies_classes)  # отфильтрованные вакансии

        if filtered_vacancies:
            print(f'По Вашему запросу найдено {len(filtered_vacancies)} вакансий')
            print()
        else:
            print('Нет вакансий, соответствующих заданным критериям')
            exit()

    else:
        filtered_vacancies = vacancies_classes

    while True:
        # Запрос у пользователя какие операции произвести с вакансиями
        query = input(('1 - Фильтрация вакансий по уровню минимального оклада\n'
                       '2 - Фильтрация вакансий по региону\n'
                       '3 - Фильтрация вакансий без опыта работы или с опытом от 1 года\n'
                       '4 - Пропуск данного шага -> '))

        if query == '4':
            break

        filtered_vacancies = user_filter(query, filtered_vacancies)

        if filtered_vacancies:
            print(f'По Вашему запросу найдено {len(filtered_vacancies)} вакансий')
            print()

        else:
            print('Нет вакансий, соответствующих заданным критериям')
            break

    sorted_vacancies = sort_vacancies(filtered_vacancies)  # Сортировка вакансий по минимальному окладу

    query = input('Хотите отфильтровать топ N вакансий с максимальным уровнем оклада?(Да/Нет) -> ')

    if query.lower() == 'да':
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        sorted_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    while True:
        # Запрос у пользователя какие операции произвести с вакансиями
        query = input('1 - Сохранить результаты работы в json-файл\n'
                      '2 - Удалить из списка вакансию по ее ID\n'
                      '3 - Вывести в консоль результат парсинга\n'
                      '4 - Завершить работу программы -> ')

        # Сохранение отфильтрованных и отсортированных вакансий в json-файл
        if query == '1':
            json_saver.save_results_to_json(sorted_vacancies)

        # Удаление вакансии из списка
        elif query == '2':
            del_id = input('Введите ID вакансии для ее удаления из списка -> ')
            json_saver.delete_vacancy(int(del_id), sorted_vacancies)

        elif query == '3':
            print_vacancies(sorted_vacancies)  # вывод в консоль результатов

        elif query == '4':
            break


if __name__ == '__main__':
    user_interaction()
