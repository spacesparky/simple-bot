Drop table subject, teacher, timetable cascade;
Create table subject(s_name text primary key);
create table teacher(id serial primary key, full_name text, subject text references subject(s_name));
create table timetable(id serial primary key, day text, subject text references subject(s_name),
					  room_numb text, start_time time, even integer, subject_num integer);
insert into subject(s_name) values ('высшая математика'),('иностранный язык'),('введение в информационные технологии'),('devops');
insert into teacher(full_name, subject) values ('Пименов В. И.','высшая математика'),('Воронова Е. В.','иностранный язык'),('Фурлетов Ю. М','введение в информационные технологии'),('Липатов В. Н.','devops');
insert into timetable(day, subject, room_numb, start_time, even, subject_num) values ('ПОНЕДЕЛЬНИК','высшая математика','311(ОП)','9:30',1,1)