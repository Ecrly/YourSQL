from core.database import *
from parse.parse import *


class Engine:

    # 初始化引擎，加载本地已有数据库
    def __init__(self):
        self.__database_names = []
        self.__database_objs = {}
        self.__current_db = None
        self.__load_databases()

    # 判断数据库是否已经存在
    def __is_exists(self, db_name):
        if db_name not in self.__database_names:
            raise Exception('%s database is not exists!' % db_name)

    # 加载本地数据库
    def __load_databases(self):
        with open('database.db', 'r') as f:
            data = f.read()
            data = json.loads(data)
            self.deserializer(data)

    # 保存数据到本地（退出时）
    def __dump_databases(self):
        with open('database.db', 'w') as f:
            f.write(json.dumps(self.serializer()))
        pass

    # 获取指定数据库
    def __get_database(self, db_name):
        self.__is_exists(db_name)
        return self.__database_objs[db_name]

    # 获取所有数据库
    def __get__database__all(self, format_type='list'):
        databases = self.__database_names
        if format_type == 'dict':
            databases = []
            for db_name in self.__database_names:
                databases.append({'database': db_name})
        return databases

    # 设定当前选中的数据库
    def __use_database(self, db_name):
        self.__is_exists(db_name)
        self.__current_db = self.__get_database(db_name)
        print('Database change, now is %s~  O(∩_∩)O' % db_name)

    # 获取当前选中的数据库
    def __get_current_db(self):
        return self.__current_db

    # 检查是否已经选中数据库
    def __check_is_choose(self):
        if self.__current_db is None:
            raise Exception('You have not choose a database')

    # 删除选定数据库
    def __drop_database(self, db_name):
        self.__is_exists(db_name)
        self.__database_names.remove(db_name)
        self.__database_objs.pop(db_name, True)
        if db_name == self.__current_db.get_name():
            self.__current_db = None
        print('Drop database %s success ' % db_name)

    # 添加数据库
    def add_database(self, db_name, database):
        if db_name in self.__database_names:
            raise Exception('%s database is already exists!' % db_name)
        self.__database_names.append(db_name)
        self.__database_objs[db_name] = database

    # 创建数据库
    def create_database(self, db_name):
        if db_name in self.__database_names:
            raise Exception('%s database is already exists!' % db_name)
        database = Database(db_name)
        self.add_database(db_name, database)
        print('Create database %s successfully' % db_name)

    # 获取当前数据库中的所有表名
    def __get_tables(self, format_type='list'):
        # 检查是否已经选中了数据库
        self.__check_is_choose()
        # 获取当前数据库中的所有表
        tables = self.__current_db.get_tables()
        if format_type == 'dict':
            tables = []
            for table_name in self.__current_db.get_tables():
                tables.append({'table': table_name})
        return tables

    # 检查当前选中的数据库中是否含指定表
    def __check_table_exist(self, table_name):
        if table_name not in self.__current_db.get_tables():
            raise Exception('Not have this table %s ' % table_name)

    # 获取指定表对象
    def __get_table_obj(self, table_name):
        self.__check_is_choose()
        self.__check_table_exist(table_name)
        return  self.__current_db.get_table_obj(table_name)

    # 给选中的数据库创建表
    def create_table(self, table_name, **kwargs):
        self.__check_is_choose()
        self.__current_db.create_table(table_name, **kwargs)
        print('Create table %s success ' % table_name)

    # 删除选定数据库中的表
    def __drop_table(self, table_name):
        self.__check_is_choose()
        self.__current_db.drop_table(table_name)
        print('Drop table %s success ' % table_name)

    # 查看指定表的结构
    def __describle_table(self, table_name):
        self.__check_is_choose()
        self.__check_table_exist(table_name)
        self.__current_db.describle_table(table_name)

    # 往指定表插入数据
    def __insert_into_table(self, table_name, kwargs):
        self.__check_table_exist(table_name)
        self.__get_table_obj(table_name).insert(**kwargs)

    # 查看指定表中的数据（目前只是全部的）
    def __select_table(self, field, table_name, conditions):
        self.__check_is_choose()
        self.__check_table_exist(table_name)
        self.__current_db.get_table_obj(table_name).select(field, conditions)

    # 序列化
    def serializer(self):
        data = {}
        for db_name, db_obj in self.__database_objs.items():
            data[db_name] = db_obj.serializer()
        return data

    # 反序列化
    def deserializer(self, data):
        for db_name, db_obj in data.items():
            self.add_database(db_name, Database.deserializer(db_obj))

    # 寻找相应的映射来执行命令
    def execute(self, statement):
        action = parse(statement)
        action_type = action['type']

        if action_type == 'exit':
            self.__dump_databases()
            return 'exit'

        if action_type == 'show':
            if action['kind'] == 'databases':
                ret = self.__get__database__all()
                if ret:
                    pt = PrettyTable(['databases'])
                    for row in ret:
                        pt.add_row([row])
                    print(pt)
                    print('%s databases is found~' % len(ret))
                else:
                    print('0 databases if found, you can use create to create database')
            elif action['kind'] == 'tables':
                ret = self.__get_tables()
                if ret:
                    title = self.__current_db.get_name() + '_' + 'talbes'
                    pt = PrettyTable([title])
                    for row in ret:
                        pt.add_row([row])
                    print(pt)
                    print('%s tables is found~' % len(ret))
                else:
                    print('0 tables if found, you can use create to create table')

        if action_type == 'desc':
            self.__describle_table(action['table_name'])

        if action_type == 'use':
            self.__use_database(action['db_name'])

        if action_type == 'create':
            if action['kind'] == 'database':
                self.create_database(action['name'])
            if action['kind'] == 'table':
                fields = action['fields']
                kwargs = {}
                for field in fields:
                    field_obj = Field(type=field['field_type'], key=field['field_keys'])
                    kwargs[field['field_name']] = field_obj
                self.create_table(action['table_name'], **kwargs)

        if action_type == 'drop':
            if action['kind'] == 'database':
                self.__drop_database(action['name'])
            elif action['kind'] == 'table':
                self.__drop_table(action['name'])

        if action_type == 'insert':
            self.__check_is_choose()
            self.__insert_into_table(action['table_name'], action['kwargs'])

        if action_type == 'select':
            self.__check_is_choose()
            field = action['field']
            table_name = action['table_name']
            conditions = action['conditions']
            self.__select_table(field, table_name, conditions)

    # 开始工作，提供while循环接收命令
    def run(self):
        while True:
            statement = input('yoursql>>')
            # try:
            ret = self.execute(statement)
            if ret:
                if ret in ['exit', 'quit']:
                    print('Goodbye~')
                    break
            else:
                pass
            # except Exception as e:
            #     print(str(e))
