from parse.parse import *

insert = "insert into student(id, name) values(1, 'chen')"
parse(insert)

create = "create table student(id int not_null unique, name str unique)"
parse(create)

select = "select id,name,age from student where id range (1,2) name = 'chen'"
parse(select)

update = "update student set id = 1, name = 'liang'"
parse(update)

delete = "delete from student where name = 'liang'"
parse(delete)

grant = "grant insert on student to chen"
parse(grant)