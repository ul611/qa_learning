
-- 1) check if there are more than 2 lines for some devices

--select device_id, 
--		payload ->> 'platform' as platform, 
--		payload ->> 'entered_at' as entered_at, 
--		updated_at 
--from devices_events de2 
--where de2.device_id in (
--	select distinct device_id
--	from devices_events de 
--	where payload ->> 'platform' is not null
--	group by device_id 
--	having count(device_id) > 2
--	)
--	and payload ->> 'platform' = 'Freebsd'
--order by device_id, updated_at

-- there is no devices that contain Freebsd in their field 'platform'
-- with more than 2 non empty field 'platform' lines 


-- 2.1) Find the right platform as the platform that isn't 'Freebsd'

--select device_id, 
--		payload ->> 'platform' as platform
--from devices_events de2 
--where de2.device_id in (
--	select distinct device_id
--	from devices_events de 
--	where payload ->> 'platform' = 'Freebsd'
--	)
--	and payload ->> 'platform' is not null
--	and payload ->> 'platform' <> 'Freebsd'


-- 2.2) Find the right platform as the platform 
--      with fullfilled 'entered_at' field

--select distinct device_id, 
--		first_value (payload ->> 'platform') over (partition by device_id order by payload ->> 'entered_at') as platform
--from devices_events de2 
--where de2.device_id in (
--	select distinct device_id
--	from devices_events de 
--	where payload ->> 'platform' = 'Freebsd'
--	)

-- 2.3) Find the right platform as the platform that isn't 'Freebsd' 
--		with joining devices_events and devices after excluding removed devices

select device_id, 
	   payload ->> 'platform' as platform
from devices_events de2 
join (select id
from devices d
where platform = 'Freebsd' and removed = false) d 
on de2.device_id = d.id 
where payload ->> 'platform' <> 'Freebsd'


select *
from devices_events
--where status = 1 and type = 1 and payload <> 'null'


select *
from devices_events de 
where created_at <> updated_at 
order by updated_at desc 

select *
from devices_events de 
where created_at = updated_at 
order by updated_at asc 

select count(*)
from devices_events de 
where created_at = updated_at and status = 1



select count(*)
from devices_events de 