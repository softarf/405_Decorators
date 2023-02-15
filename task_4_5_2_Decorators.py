# -*- coding: utf-8 -*-
#                       Декораторы.
#       Задача 2. Доработать декоратор.
#                 Путь к файлу должен передаваться в аргументах декоратора.

from datetime import datetime
import os


def it_now():
    """Печатает текущее время и дату."""
    today = datetime.today()
    wday = today.strftime('%a')
    day = today.strftime('%d')
    month = today.strftime('%b')
    year = today.strftime('%Y')
    hour = today.strftime('%H')
    minute = today.strftime('%M')
    second = today.strftime('%S')
    return f'{wday}, {day} {month} {year} {hour}:{minute}:{second}'


def logger(path):

    def __logger(old_function):

        def new_function(*args, **kwargs):

            function_name = ' ' + old_function.__name__
            str_args = ''
            if args:
                str_args = ' ' + ' '.join([str(item) for item in args])
            str_kwargs = ''
            if kwargs:
                str_kwargs = ' ' + ' '.join([str(value) for key, value in kwargs.items()])

            result = old_function(*args, **kwargs)

            str_result = ' ' + str(result)
            quote = f'{it_now()}{function_name}{str_args}{str_kwargs}{str_result}'
            with open(file=path, mode='at', encoding='utf-8') as out_file:
                # print(quote, file=out_file)    # Так тоже можно.
                out_file.write(quote + '\n')
            print(quote)

            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        print(f'\nСодержимое {path}:')

        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()

    print('\n  -- Конец --  ')
