from core.table import *
from util.serializer import *


class Database(SerializerInterface):

    # 创建数据库，空的
    def __init__(self, name):
        self.__name = name
        self.__table_names = []
        self.__table_objs = {}

    # 获取数据库名字
    def get_name(self):
        return self.__name

    # 获取所有表名
    def get_tables(self):
        return self.__table_names

    # 验证表是否存在
    def is_exists(self, table_name):
        if table_name not in self.__table_names:
            # print(self.__table_names)
            raise Exception('%s table is not exists' % table_name)

    # 获取指定表对象
    def get_table_obj(self, table_name):
        self.is_exists(table_name)
        return self.__table_objs[table_name]

    # 删除表
    def drop_table(self, table_name):
        self.is_exists(table_name)
        self.__table_names.remove(table_name)
        self.__table_objs.pop(table_name, True)

    # 添加表
    def add_table(self, table_name, table):
        if table_name in self.__table_names:
            raise Exception('%s table is already exists!' % table_name)
        self.__table_names.append(table_name)
        self.__table_objs[table_name] = table
        # print('enen')

    # 创建表
    def create_table(self, table_name, **kwargs):
        if table_name in self.__table_names:
            raise Exception('%s table is already exists!' % table_name)
        table = Table(**kwargs)
        self.add_table(table_name, table)

    # 向指定表插入数据
    def insert_into_table(self, table_name, **kwargs):
        self.is_exists(table_name)
        self.__table_objs[table_name].insert(**kwargs)

    # 查看指定表结构
    def describle_table(self, table_name):
        self.is_exists(table_name)
        self.__table_objs[table_name].describle()

    # 查看指定表数据
    def select_table(self, table_name):
        self.is_exists(table_name)
        self.__table_objs[table_name].select()

    # 序列化
    def serializer(self):
        data = {
            'name': self.__name,
            'tables': {}
        }
        for table_name, table_obj in self.__table_objs.items():
            data['tables'][table_name] = table_obj.serializer()
        return data

    # 反序列化
    @staticmethod
    def deserializer(data):
        database = Database(data['name'])
        for table_name, table_obj in data['tables'].items():
            database.add_table(table_name, Table.deserializer(table_obj))
        return database
