from core.field import *
from prettytable import PrettyTable
from util.case import *


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
    def select(self, fields, conditions):

        # 如果是*查找所有字段
        if '*' in fields:
            fields = self.__field_names
        else:
            for field in fields:
                if not field in self.__field_names:
                    raise Exception('%s you selected is not in the table!' % field)

        match_index = self.__parse_conditions(conditions)

        pt = PrettyTable(fields)
        for i in match_index:
            val_row = []
            for field_name in fields:
                val_row.append(self.__field_objs[field_name].get_values()[i])
            pt.add_row(val_row)
        print(pt)
        print('%s rows in set' % len(match_index))

    # 更新表中的数据
    def update(self, data, conditons):
        match_index = self.__parse_conditions(conditons)
        for name, value in data.items():
            if name not in self.__field_names:
                raise Exception('Field %s you want to update is not exists!' % name)
            self.__field_objs[name].update(value, match_index)
        print('%s rows were updated' % len(match_index))

    # 解析查询条件返回符合条件的索引
    def __parse_conditions(self, conditions):

        # 如果没有查询条件，所有的都可以
        if not conditions:
            match_index = range(0, self.__row)

        # 解析查询条件
        else:
            # 获得所有条件针对的字段
            name_tmp = []
            for name in conditions.keys():
                if name not in self.__field_names:
                    raise Exception('%s field in where is not eixits!' % name)
                name_tmp.append(name)

            # 存放上次条件匹配成功的索引
            match_tmp = []

            # 存放所有条件匹配成功后的索引
            match_index = []

            # 首次循环的标志位，二次循环只需验证上次循环的结果
            is_first = True

            for field_name in name_tmp:

                # 获取字段的数据及类型进行验证条件
                values = self.__get_field_value(field_name)
                data_type = self.__get_field_type(field_name)

                # 获取条件
                case = conditions[field_name]

                # 检查条件类型
                if not isinstance(case, BaseCase):
                    raise Exception('Type error: value must be "Case" object')

                if is_first:
                    length = self.__field_objs[field_name].get_row()

                    for i in range(0, length):
                        if case(values[i], data_type):
                            match_tmp.append(i)
                            match_index.append(i)

                    is_first = False

                    continue

                for i in match_tmp:
                    if not case(values[i], data_type):
                        match_index.remove(i)

                match_tmp = match_index

        return match_index

    # 获取指定字段的所有数据内容
    def __get_field_value(self, field_name):
        return self.__field_objs[field_name].get_values()

    # 获取指定字段的数据类型（为了和where条件中的数据类型做验证）
    def __get_field_type(self, field_name):
        return self.__field_objs[field_name].get_type()

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

