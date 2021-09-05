from tfidf.models import Word
from WG.settings import WORDS_ON_PAGE
from .counter import Counter
from math import log10


def update_table_data(new_words: list['str']) -> set['str']:
    db_words = set()
    for db_w in Word.objects.all():
        db_w.tf_last = new_words.count(db_w.word)  # встреч в текущем файле
        if db_w.tf_last:
            db_w.met_count += 1  # количество файлов в которых встречено слово
        db_words.add(db_w.word)
        db_w.save()
    return db_words


def fill_table(new_words: list['str'], exist_words: set['str']) -> None:
    new_unique = set(new_words) - exist_words
    unique_count = len(new_unique)
    if unique_count != 0:
        add_count = abs(len(exist_words) - WORDS_ON_PAGE)
        add_count = unique_count if unique_count < add_count else add_count
        for i in range(add_count):
            w = new_unique.pop()
            new_w = Word(word=w, tf_last=new_words.count(w), met_count=1)
            new_w.save()


def collect_table_rows(by_increase=False) -> list[tuple[str, int, float]]:
    counter = Counter()
    file_count = counter.get_current_value()
    rows = []
    for db_w in Word.objects.all():
        idf = log10(file_count / db_w.met_count)
        idf = round(idf, 2)  # округление до двух знаков
        rows.append((db_w.word, db_w.tf_last, idf))
    rows = sorted(rows, key=lambda row: row[2])  # сортировать по idf
    if not by_increase:
        rows.reverse()
    return rows


def flush_table() -> None:
    Word.objects.all().delete()
