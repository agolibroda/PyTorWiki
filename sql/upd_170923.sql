-- накатываем первые изменения структуры.

-- поменяем тип столбца, что бы в нем хранить статьи без обработки бейс-64.

ALTER TABLE articles
	ADD COLUMN article_source_tmp bytea;

update articles SET 
	article_source_tmp = decode(article_source, 'base64') ;

 ALTER TABLE articles
	ALTER COLUMN article_source TYPE bytea USING article_source_tmp::bytea; 
	
 ALTER TABLE articles
	DROP COLUMN article_source_tmp; 
		
-- вводим понятие "рабочий стол" как таковой  
-- в нем будет ИД, публичный ключ для возможного шифрования данных,
-- и тип стола - или персональный стол автора, или групповой   


DROP SEQUENCE IF EXISTS dt_header_id_seq CASCADE;
CREATE SEQUENCE IF NOT EXISTS dt_header_id_seq;

DROP TYPE IF EXISTS dt_type CASCADE;
CREATE TYPE dt_type AS enum('author','group');


DROP TABLE IF EXISTS dt_headers CASCADE;
CREATE TABLE IF NOT EXISTS dt_headers (
  dt_header_id int PRIMARY KEY not null,
  dt_header_type dt_type  NOT NULL DEFAULT 'author',
  public_key bytea NOT NULL
);
  
	
CREATE OR REPLACE FUNCTION trigger_dt_header_lns () RETURNS trigger AS $$ 
BEGIN 
      If  NEW.dt_header_id = 0 OR NEW.dt_header_id IS NULL then 
      NEW.dt_header_id = nextval('dt_header_id_seq');
      end if;

return NEW;
END; 
$$ LANGUAGE  plpgsql;

-- Создание триггера
CREATE TRIGGER dt_header_bi 
	BEFORE INSERT ON dt_headers FOR EACH ROW 
	EXECUTE PROCEDURE trigger_dt_header_lns ();


CREATE INDEX dt_header_id_ind ON dt_headers (dt_header_id);
CREATE INDEX dt_header_type_ind ON dt_headers (dt_header_type);

INSERT INTO  dt_headers (dt_header_id, dt_header_type, public_key ) VALUES 
(1,	'author',	'');

SELECT setval('dt_header_id_seq', COALESCE((SELECT MAX(dt_header_id)+1 FROM dt_headers), 1), false);
ALTER SEQUENCE dt_header_id_seq OWNED BY dt_headers.dt_header_id;


DROP SEQUENCE IF EXISTS author_author_id_seq CASCADE;
DROP TRIGGER IF EXISTS author_bi ON authors CASCADE;

DROP FUNCTION IF EXISTS  trigger_author_before_lns ();

ALTER TABLE IF EXISTS authors
    RENAME COLUMN author_id TO dt_header_id;
    
ALTER TABLE IF EXISTS authors
	ADD CONSTRAINT author_dt_header
	FOREIGN KEY ( dt_header_id ) REFERENCES dt_headers ( dt_header_id ); 
	
--
--	
DROP SEQUENCE IF EXISTS groups_group_id_seq CASCADE;
	
DROP TRIGGER IF EXISTS groups_bi ON groups CASCADE;


DROP FUNCTION IF EXISTS trigger_groups_before_lns ();

ALTER TABLE IF EXISTS groups
    RENAME COLUMN group_id TO dt_header_id;
    
ALTER TABLE IF EXISTS groups
	ADD CONSTRAINT groups_dt_header
	FOREIGN KEY ( dt_header_id ) REFERENCES dt_headers ( dt_header_id ); 


-- нужна табличка для хранения всез приватных ключей для  всех групп и всех авторов - участников. 
-- ключ (всяий ключ закыт публичным ключем автора. )


ALTER TABLE IF EXISTS members
	ADD COLUMN private_key bytea NOT NULL, -- приватный ключ надо добавить в профиль Автора в руппе - для каждого автора группы - его личная версия приватного ключа!

	ADD CONSTRAINT members_author_id_fk
	FOREIGN KEY ( author_id ) REFERENCES dt_headers ( dt_header_id ),
	 
	ADD CONSTRAINT members_group_id_fk
	FOREIGN KEY ( group_id ) REFERENCES dt_headers ( dt_header_id ); 
 
CREATE UNIQUE INDEX members_author_id_group_id_ind ON members (author_id, group_id);


 
-- приватный ключ надо добавить в профиль Автора - 
-- и закрыть его там  - на проль пользователя!!!!	
-- - при смене пароля - перезакрывать и Приватный ключ!!!!!
--  в случае потери пароля - надо сравнить Хеи приватных ключей, того, что сохранен, и того хеша, что в базе, - если совпало, 
-- тогда все норм и можно менять пароль, брать сохраненный приватный ключ, закрывать его на новом пароле, и класть в нужное место :-)   

ALTER TABLE authors
	ADD COLUMN private_key bytea; -- after sha_hash;

ALTER TABLE authors
	ADD COLUMN private_key_hash bytea; -- after sha_hash;

--ALTER TABLE groups	
--	  sha_hash character varying(66) NOT NULL primary key;
	  
ALTER TABLE groups ADD PRIMARY KEY (sha_hash);
	
  

	
	
	
	
	