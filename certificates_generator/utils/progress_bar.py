class ProgressBar:

    def __init__(self, length, max_value: int) -> None:
        self._value = 0
        self._length = length
        self._max_value = max_value if max_value != 0 else 100

    def increase(self, step: int = 1) -> None:
        assert (0 <= self._value + step <= self._max_value)
        self._value += step
        per_percent = self._length / self._max_value
        progress = round((self._value / self._max_value)*100, 2)
        progress_bar = ('▇' * int(per_percent * self._value)).ljust(self._length, '-')
        print(f'Прогресс:[{progress_bar}] {progress}%', end='\r')
    
    def flush(self) -> None:
        ADDITIONAL_CHARS_LEN = 18
        print(' ' * (self._length + ADDITIONAL_CHARS_LEN), end='\r')
