from parse.parse import *

insert = "insert into student(id, name) values(1, 'chen')"
parse(insert)

create = "create table student(id int not_null unique, name str unique)"
parse(create)

select = "select * from student where id range (1,2) name = 'chen'"
parse(select)