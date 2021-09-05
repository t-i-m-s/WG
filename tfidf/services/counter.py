from WG.settings import BASE_DIR


class Counter:
    counter_file_path = BASE_DIR / 'tfidf/services/file_count.txt'

    def increase_counter(self) -> None:
        with open(self.counter_file_path) as fc:
            file_count = int(fc.read()) + 1
        with open(self.counter_file_path, 'w') as fc:
            fc.write(str(file_count))

    def get_current_value(self) -> int:
        with open(self.counter_file_path) as fc:
            return int(fc.read())  # количество проверенных файлов

    def reset_counter(self) -> None:
        with open(self.counter_file_path, 'w') as fc:
            fc.write(str(0))
