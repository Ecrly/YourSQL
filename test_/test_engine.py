from core.engine import *

engine = Engine()
use = "use party"
create = "create table class(id int auto_increment, name str)"
desc = "desc class"
insert = "insert into class() values()"
select = "select class"
show_table = "show tables"
drop_table = "drop table student"
drop_database = "drop database party"
show_databases = "show databases"
engine.execute(use)
engine.execute(create)
engine.execute(desc)
engine.execute(select)
engine.execute(insert)
engine.execute(select)
engine.execute(insert)
engine.execute(select)
engine.execute(show_table)
engine.execute(drop_table)
engine.execute(show_table)
engine.execute(drop_database)
engine.execute(show_databases)