from core.engine import *

engine = Engine()
use = "use party"
create = "create table class(id int auto_increment, name str, age int null, sex str)"
desc = "desc class"
insert1 = "insert into class(name, age, sex) values('chen', 12, 'man')"
insert2 = "insert into class(name, age, sex) values('liang', 13, 'nv')"
insert3 = "insert into class(name, age, sex) values('ni', 15, 'man')"
insert4 = "insert into class(name, age, sex) values('hao', 17, 'man')"
select1 = "select * from class"
select2 = "select id,name from class where id <= 2"

show_table = "show tables"
drop_table = "drop table student"
drop_database = "drop database party"
show_databases = "show databases"
engine.execute(use)
engine.execute(create)
engine.execute(desc)
engine.execute(insert1)
engine.execute(insert2)
engine.execute(insert3)
engine.execute(insert4)
engine.execute(select1)
engine.execute(select2)