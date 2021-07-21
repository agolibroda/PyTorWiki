SELECT 
dt_headers.dt_header_id,  author_login, author_name, author_surname, author_role, author_phon, 
author_email, author_create, dt_headers.public_key  
FROM authors, dt_headers 
WHERE   dt_headers.dt_header_id = authors.dt_header_id  
AND actual_flag = 'A'  
ORDER BY  dt_header_id

psql -U postgres -d py_wiki -c "SELECT * FROM articles "


SELECT * FROM articles 