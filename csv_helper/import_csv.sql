load data local infile '${filePath}' 
into table ${table_name}
fields terminated by ','
lines terminated by '\n'
IGNORE 1 ROWS
(@id,@name,@flag)
SET id=@id,
name=@name,
flag=IF(@flag = "true", 1, 0),
update_time=NOW();