from core.field import *
from prettytable import PrettyTable


class Table(SerializerInterface):

    # 创建表：kwargs格式为：field_name = field_obj
    def __init__(self, **kwargs):
        self.__field_names = []
        self.__field_objs = {}
        self.__row = 0
        self.__col = 0
        for field_name, field_obj in kwargs.items():
            if field_name in self.__field_names:
                raise Exception('Field %s is already exists' % field_name)
            self.__field_names.append(field_name)
            self.__field_objs[field_name] = field_obj
            self.__col += 1

    # 添加字段
    def add_field(self, field_name, field_obj, values=None):
        # 检查字段名是否已经存在
        if field_name in self.__field_names:
            raise Exception('Field %s is already exists!' % field_name)
        self.__field_names.append(field_name)
        # 检查字段类型
        if not isinstance(field_obj, Field):
            raise Exception('field type wrong!!')
        self.__field_objs[field_name] = field_obj
        # 如果需要在此处手动添加数据内容，不过一般都是在Field处理
        if values:
            self.__row = len(values)
            for value in values:
                self.__field_objs[field_name].add(value)
        # 设置row和col
        self.__col = len(self.__field_names)
        self.__row = max(self.__field_objs[field_name].get_row(), self.__row)

    # 查看表结构
    def describle(self):
        pt = PrettyTable(['Field', 'Type', 'Key'])
        for field_name in self.__field_objs:
            pt.add_row([field_name, self.__field_objs[field_name].get_type(), self.__field_objs[field_name].get_key()])
        print(pt)
        print('%s rows in set' % self.__col)

    # 向表中插入数据： kwargs格式为：field_name=value
    def insert(self, **kwargs):
        for field_name in kwargs.keys():
            if field_name not in self.__field_names:
                raise Exception('Not have this field %s' % field_name)
        for field_name in self.__field_names:
            value = None
            if field_name in kwargs:
                value = kwargs[field_name]
            try:
                self.__field_objs[field_name].add(value)
            except Exception as e:
                raise Exception(field_name, str(e))

        self.__row += 1
        print('Insert success!!')

    # 查看表中数据
    def select(self, field, conditions):
        pt = PrettyTable(self.__field_names)
        for i in range(0, self.__row):
            val_row = []
            for field_name in self.__field_objs:
                val_row.append(self.__field_objs[field_name].get_values()[i])
            pt.add_row(val_row)
        print(pt)
        print('%s rows in set' % self.__row)

    # 序列化
    def serializer(self):
        data = {}
        for field_name in self.__field_names:
            data[field_name] = self.__field_objs[field_name].serializer()
        return data

    # 反序列化
    @staticmethod
    def deserializer(data):
        table = Table()
        for field_name, field_obj in data.items():
            table.add_field(field_name, Field.deserializer(field_obj))
        return table

