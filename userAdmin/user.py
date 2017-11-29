from userAdmin.authority import *
from util.serializer import *


class User(SerializerInterface):

    def __init__(self, name, pwd, auz, privs, dbs):
        self.__name = name
        self.__pwd = pwd
        self.__auz = auz
        self.__privs = privs
        self.__dbs = dbs
        if not isinstance(self.__privs, list):
          self.__privs = [self.__privs]
        if not isinstance(self.__dbs, list):
          self.__dbs = [self.__dbs]
          for priv in self.__privs:
            if priv not in PRIV:
                raise Exception("Not have this privilege : %s !" % priv)

    def get_name(self):
        return self.__name

    def get_pwd(self):
        return self.__pwd

    def get_privs(self):
        return self.__privs

    def add_priv(self, priv, db):
        if priv in self.__privs:
            raise Exception('%s privilege is exists!' % priv)
        self.__privs.append(priv)
        self.__dbs.append(db)

    def get_auz(self):
        return self.__auz

    def check_pwd(self, pwd):
        return pwd == self.__pwd

    def check_priv(self, priv, db):
        if self.__auz == 'root':
            return True
        if 'all' in self.__privs and 'all' in self.__dbs:
            return True
        elif 'all' in self.__privs and db in self.__dbs:
            return True
        elif priv in self.__privs and 'all' in self.__dbs:
            return True
        elif priv in self.__privs and db in self.__dbs:
            return True
        else:
            raise Exception('You dont have priv '+ priv + ' on ' + db + ' !!')

    def serializer(self):
        return {
            'name': self.__name,
            'pwd': self.__pwd,
            'auz': self.__auz,
            'privs': self.__privs,
            'dbs': self.__dbs,
        }

    @staticmethod
    def deserializer(data):
        user = User(data['name'], data['pwd'], data['auz'], data['privs'], data['dbs'])
        return user


