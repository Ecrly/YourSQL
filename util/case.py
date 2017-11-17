def __range(data, condition):
    return  condition[0] >= data <= condition[1]

symbol_map = {
    range: __range,
}


class BaseCase():
    def __init__(self, condition, symbol):
        self.condition = condition
        self.symbol = symbol

    def __call__(self, data, data_type):
        pass


class RangeCase(BaseCase):
    def __init__(self, start, end):
        start = int(start)
        end = int(end)
        if start > end:
            raise Exception('start must < end in range tuple!')
        super().__init__((start, end), symbol='range')

    def __call__(self, data):
        if not isinstance(self.condition, tuple):
            raise Exception('Not a tuple condition')
        return symbol_map[self.symbol](data, self.condition)
