from core.engine import *

engine = Engine()
create_db = "create database party"
use = "use party"
create = "create table class(id int auto_increment, name str, age int null, sex str)"
desc = "desc class"
insert1 = "insert into class(name, age, sex) values('chen', 12, 'man')"
insert2 = "insert into class(name, age, sex) values('liang', 13, 'nv')"
insert3 = "insert into class(name, age, sex) values('ni', 15, 'man')"
insert4 = "insert into class(name, age, sex) values('hao', 17, 'man')"
select1 = "select * from class"
select2 = "select id, name from class where id <= 2"
update1 = "update class set sex = 'zhong',name = 'en' where id range (1,3)"
delete1 = "delete from class where id range (1,3)"
show_table = "show tables"
drop_table = "drop table student"
drop_database = "drop database party"
show_databases = "show databases"
# engine.execute(create_db)
# engine.execute(use)
# engine.execute(create)
# engine.execute(desc)
# engine.execute(insert1)
# engine.execute(insert2)
# engine.execute(insert3)
# engine.execute(insert4)
# engine.execute(select1)
# engine.execute(select2)
# engine.execute(update1)
# engine.execute(select1)
# engine.execute(delete1)
# engine.execute(select1)
# engine.execute(insert1)
# engine.execute(insert2)
# engine.execute(select1)
# engine.execute('exit')

engine.execute('create database test')
engine.execute('use test')
engine.execute("create table test(id int auto_increment, name str not_null, sex str, age int)")
engine.execute('desc test')
engine.execute("insert into test(name,sex,age) values('chen','nan',17)")
engine.execute("insert into test(name,sex,age) values('liang','nv',17)")
engine.execute("insert into test(name,sex) values('ni','nan')")
engine.execute("insert into test(name,age) values('hao',17)")
engine.execute("select * from test")
engine.execute("update test set sex = 'nan',name = 'en' where id = 4")
engine.execute("select * from test")