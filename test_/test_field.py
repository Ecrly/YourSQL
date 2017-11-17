from core.field import *
from core.engine import *
import base64

int = Field(type='int', key='null')
string = Field(type='str', key='unique')

table = Table(id=int, name=string)
table.describle()
table.insert(id=1, name='chen')
table.insert(id=2, name='liang')
table.select()

database = Database('school')
database.add_table('student', table)
database.describle_table('student')
database.insert_into_table('student', id=3, name='wu')
database.select_table('student')
data = database.serializer()
print(data)
database = Database.deserializer(data)
database.describle_table('student')

print('********************************************')
engine = Engine()
print(engine.serializer())
