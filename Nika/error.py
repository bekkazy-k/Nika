import traceback


def handle():
    """
    Возвращает текст ошибки без ковычек, чтобы можно было записывать в  БД
    :return: Текст ошибки
    """
    formatted_lines = traceback.format_exc().splitlines()
    return f'{formatted_lines[-1]}; {formatted_lines[-2].replace(" ", "")}; {formatted_lines[-3].replace(" ", "", 2)}'


def error_handler(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            formatted_lines = traceback.format_exc().splitlines()
            text = f'Error: {formatted_lines[-1]}; Method: {formatted_lines[-2].replace(" ", "")}; ' \
                   f'{formatted_lines[-3].replace(" ", "", 2)}'
            print("Error!", text)
            return None
    return func_wrapper


# @error_handler
# def hello(a, b):
#     print(a/b)
#
#
# hello(5, 0)
