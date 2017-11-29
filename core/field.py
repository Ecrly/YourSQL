from util.constant import *
from util.serializer import *
from util.encode import *


class Field(SerializerInterface):

    def __init__(self, **kwargs):
        self.__type = kwargs['type']
        self.__check_type_exits()
        self.__keys = kwargs.get('key', 'null')
        if not isinstance(self.__keys, list):
            self.__keys = [self.__keys]
        if len(self.__keys) == 0:
            self.__keys.append('null')
        self.__default = kwargs.get('default', None)
        self.__check_keys()
        self.__row = 0
        self.__values = []

    # 向字段中插入数据
    def add(self, value):

        # 如果值为空就用默认值，注意默认值也可能为空，需要进一步检查
        if value is None:
            value = self.__default

        # 检查值与键是否符合
        value = self.__check_value(value)

        # 检查值与类型是否符合
        self.__check_type(value)

        # 插入数据
        self.__values.append(value)
        self.__row += 1

    # 更新数据
    def update(self, value, index):

        # 检查值与键是否符合
        value = self.__check_value(value)

        # 检查值与类型是否符合
        self.__check_type(value)

        # 检查索引合法性
        self.__check_index(index)

        # 更新数据
        self.__values[index] = value

    # 删除数据
    def delete(self, index):

        # 检查索引合法性
        self.__check_index(index)

        # 删除数据
        self.__values.pop(index)
        self.__row -= 1

    def __check_type_exits(self):
        if self.__type not in TYPE:
            raise Exception('Not this type %s' % self.__type)

    def __check_keys(self):

        # 检查指定约束是否合法
        for key in self.__keys:
            if key not in KEY:
                raise Exception('Not have this key %s' % key)

        # primary_key和null不共存
        if 'primary_key' in self.__keys and 'null' in self.__keys:
            raise Exception("primary_key can't be null!")

        # auto_increment必须是int类型
        if 'auto_increment' in self.__keys:
            if self.__type != 'int':
                raise Exception('auto_increment must be int type!')

        # unique不能设默认值
        if 'unique' in self.__keys:
            if self.__default is not None:
                raise Exception("unique type can't has default value")

        # not_null和null不能共存
        if 'not_null' in self.__keys and 'null' in self.__keys:
            raise Exception("'not_null' and 'null' can't exists in the same field!")

        # 检查default是否符合类型
        if not isinstance(self.__default, TYPE[self.__type]) and self.__default is not None:
            raise Exception('default type wrong, field is %s '% self.__type)

    def __check_value(self, value):

        # 如果是自增类型的
        if 'auto_increment' in self.__keys:
            # 可以不给值，直接默认往后加
            if value is None:
                if self.__row == 0:
                    value = 1
                else:
                    value = self.__values[self.__row - 1] + 1
            # 如果给值了，那就有点麻烦，因为他可能和前面重复，即使和前面不重复也可能和后面重复
            # 草他妈的不管了，直接给异常了,他妈的自增还指定数据有病，肯定有病
            if value in self.__values:
                # value = self.__values[self.__row - 1] + 1
                raise Exception('value %s exists! and the field type is auto_increment!!' % value)

        # 如果是主键或者非空
        if ('primary_key' in self.__keys or 'not_null' in self.__keys) and value is None:
            raise Exception("value cant be None")

        # 如果是主键或者不重复
        if ('primary_key' in self.__keys or 'unique' in self.__keys) and value in self.__values:
            raise Exception("value %s exists!!" % value)

        return value

    def __check_type(self, value):

        # 如果不是None又不符合类型，报异常
        if value is not None and not isinstance(value, TYPE[self.__type]):
            raise Exception('Type error, field is %s' % self.__type)

    def __check_index(self, index):
        if not -index < self.__row > index:
            raise Exception('Not have this element')

    def __str__(self):
        return '<' + self.__type + ',' + self.__keys + '>'

    def get_type(self):
        return self.__type

    def get_key(self):
        return self.__keys

    def get_values(self):
        return self.__values

    def get_row(self):
        return self.__row

    def serializer(self):
        return {
            'type': self.__type,
            'key': self.__keys,
            'values': self.__values,
            'default': self.__default,
        }

    @staticmethod
    def deserializer(data):
        default = data.get('default', None)
        field = Field(type=data['type'], key=data['key'], default=default)
        for val in data['values']:
            field.add(val)
        return field


