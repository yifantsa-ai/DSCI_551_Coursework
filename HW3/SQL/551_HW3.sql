use 551face;

select task, count(f.id) 
from model as m, file as f
where m.id = f.model_id
group by task
order by count(f.id) desc, m.task asc;

select task
from model
group by task
having count(id) >= 2
order by task asc;

select distinct m1.task
from model as m1
join model as m2
on m1.task = m2.task and m1.user_id != m2.user_id
order by m1.task asc;

select avg(size)
from file as f, model as m
where f.model_id = m.id and m.task = 'speech recognition'
and f.file_path like '%.safetensors';

with fd as(
	select file_id, count(user_id) as d_times
    from download
    group by file_id
),
md as(
	select max(d_times) as max_times
    from fd
)
select file_id
from fd, md
where fd.d_times = md.max_times
order by file_id asc;

select distinct d1.user_id
from download as d1
join download as d2
on d1.user_id = d2.user_id
and d1.file_id = 'f1' and d2.file_id = 'f2'
order by d1.user_id asc;

(select distinct user_id
from download
where file_id = 'f1'
order by user_id asc)
intersect
(select distinct user_id
from download
where file_id = 'f2'
order by user_id asc);

with mp as(
	select max(num_params) as max_p
    from model
    where task = 'language generation'
)
select model.name
from model, mp
where model.task = 'language generation'
and mp.max_p = model.num_params;

select d.user_id, d.file_id
from download as d, file as f, model as m
where d.file_id = f.id and f.model_id = m.id and m.user_id = d.user_id
order by d.user_id asc, d.file_id asc
limit 5;