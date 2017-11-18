from util.constant import *


def __range(data, condition):
    return condition[0] <= data <= condition[1]


def __in(data, condition):
    return data in condition


def __not_in(data, condition):
    return data not in condition


def __is(data, condition):
    return data == condition


def __is_not(data, condition):
    return data != condition


def __greater(data, condition):
    return data > condition


def __less(data, condition):
    return data < condition


def __greater_and_is(data, condition):
    return data >= condition


def __less_and_is(data, condition):
    return data <= condition


def __like(data, condition):
    tmp = condition.split('%')
    length = len(tmp)
    if length == 3:
        condition = tmp[1]
    elif length == 2:
        raise Exception('Syntax Error: % !')
    elif length == 1:
        condition = tmp[0]
    return condition in data

symbol_map = {
    'range': __range,
    'in': __in,
    'not_in': __not_in,
    '=': __is,
    '!=': __is_not,
    '>': __greater,
    '<': __less,
    '>=': __greater_and_is,
    '<=': __less_and_is,
    'like': __like,
}


# 普通情况的基类
class BaseCase:
    def __init__(self, condition, symbol):
        self.condition = condition
        self.symbol = symbol

    def __call__(self, data, data_type):

        # 转类型，因为条件中的int都是以str的形式输入的
        self.condition = TYPE[data_type](self.condition)
        if isinstance(self.condition, str):
            self.condition = self.condition.replace('"', '').replace("'", "")

        return symbol_map[self.symbol](data, self.condition)


# list类型情况的基类（in not_in）
class BaseListCase(BaseCase):

    def __call__(self, data, data_type):
        if not isinstance(self.condition, list):
            raise Exception('Condition type error, value must be %s' % data_type)

        condition = []

        # 对于list类型的条件，我们需要把其中的每一种元素都取出来转类型
        for elem in self.condition:
            elem = TYPE[data_type](elem)
            if isinstance(elem, str):
                elem = elem.replace('"', '').replace("'", "")
            condition.append(elem)

        return symbol_map[self.symbol](data, condition)


class RangeCase(BaseCase):
    def __init__(self, start, end):
        try:
            start = int(start)
            end = int(end)
        except:
            raise Exception('Range type must be int!')
        if start > end:
            raise Exception('start must < end in range tuple!')
        super().__init__((start, end), symbol='range')

    def __call__(self, data, data_type):
        if not isinstance(self.condition, tuple):
            raise Exception('Not a tuple condition')
        if data_type != 'int':
            raise Exception('The field is not int, you cant use range!')
        return symbol_map[self.symbol](data, self.condition)


class InCase(BaseListCase):
    def __init__(self, condition):
        super().__init__(condition, 'in')


class NotInCase(BaseListCase):
    def __init__(self, condition):
        super().__init__(condition, 'not_in')


class IsCase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, '=')


class IsNotCase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, '!=')


class GreaterCase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, '>')


class LessCase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, '<')


class GAECase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, '>=')


class LAECase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, '<=')


class LikeCase(BaseCase):
    def __init__(self, condition):
        super().__init__(condition, 'like')

    def __call__(self, data, data_type):
        self.condition = TYPE[data_type](self.condition)
        return symbol_map[self.symbol](str(data), self.condition)
