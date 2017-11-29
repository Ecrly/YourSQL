from userAdmin.user import *
from util.serializer import *
import json


class Admin(SerializerInterface):
    def __init__(self):
        self.__user_names = []
        self.__user_objs = {}
        self.__cur_user = None
        self.__load_users()

    def __load_users(self):
        with open('admin.db', 'r') as f:
            data = f.read()
            data = json.loads(data)
            self.deserializer(data)

    def dump_user(self):
        with open('admin.db', 'w') as f:
            f.write(json.dumps(self.__serializer()))

    def get_cur_user(self):
        return self.__cur_user

    def __add_user(self, user_name, user_obj):
        if user_name in self.__user_names:
            raise Exception('%s user is already exists!' % user_name)
        self.__user_names.append(user_name)
        self.__user_objs[user_name] = user_obj

    def create_user(self, name, pwd):
        user = User(name, pwd, 'client', [], [])
        self.__add_user(name, user)
        print('Create user %s successful!' % name)

    def grant_user(self, priv, db, user):
        if user not in self.__user_names:
            raise Exception('Not have this user %s !' % user)
        self.__user_objs[user].add_priv(priv, db)
        print('Grant priv success')

    def check_user(self, user_name, user_pwd):
        if user_name not in self.__user_names:
            raise Exception('%s not exists!' % user_name)
        if self.__user_objs[user_name].check_pwd(user_pwd):
            self.__cur_user = self.__user_objs[user_name]
        else:
            raise Exception('Password is wrong!!')

    def check_priv(self, action, db_name):
        if self.__cur_user is None:
            raise Exception('Please login first!')
        self.__cur_user.check_priv(action, db_name)

    def check_auz(self):
        return self.__cur_user.get_auz()

    def show_users(self):
        print(self.__serializer())

    def __serializer(self):
        users = {}
        for user_name, user_obj in self.__user_objs.items():
            users[user_name] = user_obj.serializer()
        return users

    def deserializer(self, data):
        for user_name, user_obj in data.items():
            self.__add_user(user_name, User.deserializer(user_obj))

