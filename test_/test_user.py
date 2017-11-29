from userAdmin.user import *
priv = ['select', 'insert']

user = User('root', 'root', priv)


print(user.get_name())
print(user.get_name())
print(user.get_privs())
print(user.serializer())
print()
print()
print()
print()
User.deserializer(user.serializer())