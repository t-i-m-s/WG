from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.core.files.uploadedfile import UploadedFile
from tfidf.services.counter import Counter
from tfidf.services import file_handle_funcs as fhf
from tfidf.services import word_handle_funcs as whf


counter = Counter()


def main_page(request):
    if request.method == 'GET':
        file_count = counter.get_current_value()  # сколько файлов уже проверено
        rows = whf.collect_table_rows()  # ряды для вывода в браузере
        return render(request, 'main.html', context={'rows': rows,
                                                     'checked': file_count})
    elif request.method == 'POST':
        if request.GET.get('action') == 'clear':
            whf.flush_table()  # очистить таблицу
            counter.reset_counter()  # сброс счетчика
            return HttpResponseRedirect(request.path)

        file: UploadedFile = request.FILES.get('file')
        if not fhf.name_valid(file.name):
            return render(request, 'main.html', context={'error': 'Invalid file format!'})
        new_words = fhf.get_words(file)  # получение слов из файла с помощью regex
        exist_words = whf.update_table_data(new_words)  # обновление данных слов в бд
        whf.fill_table(new_words, exist_words)  # добавление новых уникальных слов до 50
        counter.increase_counter()  # увеличить счетчик на +1 проверенный файл
        return HttpResponseRedirect(request.path)
    else:
        return HttpResponseNotAllowed(permitted_methods=('GET', 'POST'))
