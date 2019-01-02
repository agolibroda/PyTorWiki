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
	
  
--UPDATE articles SET
--article_source = '\\x789c95946d6bdb3010c7df17fa1d5441dfd5d152061d25368cb683c2d80a6dc7c61841b52ff111d9f2a473d207f2dd77726cd72923cb5ed8b2a4bb9ffff7204d8e2ebf5edcfdb8b912391526393c98f423e82c8c05901669ae9d078ae5fddda7e883e4f56e2727aa22f85de33296dfa3fb8fd1852d2a4df860408ad4960425bb5d5fc590cde124cd9d2d201ecb9e5c6a9ecb25c2aab28e062e2bcc288f3358620a513339115822a136914fb561cae85dc331582e8403134b9f3323ad492063a4c81dcc62a93cb19e5461a1e7e055d8f26aa697e163c4af370c5d550622b2759a477b63aa72fe4f8cc767f0b13c3b7d3c3bdd071a3596ff831e8fdf3ff2b317bcb5edf0db69a427033e07a0b7a8152e70947a2f053d555c3782475261be41109281e4e5a5d28ecb4ae0fc483bf633d08dd3c664bd9ea88ded761b64e05387156108aaef849d3c5d963668b3e57addaa505deb3ed8ec298c192e0566b10c73395c0886e0faa526ee58ce8cd574ee709ed386f8722c7026d2da39d633ad3d3871bc6e7ea5bbfc54accd96da4c3984c5946c25939b76495c6abf1077b69a28dde1c0786818af045d53ae8c9d6329935b9c97dcecc14190e54c1495f5a02043dab89759a740b1f0e6b88e935796dcb3063ae1648d9301e6288a4413e0f5edb9f8624b105134cc585b9436d3c1bab059cddd22ba9f84fb63e0941aedb935dbdd8ddff65657158ecbe995d8a1dbdbdaa56dde1e5cd23ddb42d40cf93d35e869a0652b1fc1e233efafd7adabdaeddc6767185056844a1d1efcecd3de95699fdccbe48a8b2928472fc2a10ab5f83584ed84601608dff8d214da183eb44bf47c027c4be9f5b6e3df57bad3a19a1bff0f8308fa84',
--sha_hash = '328e81f9b15b72b3a4155aefdc7f271e8f39d75dcdea182193b9033d78d5fe57'
--WHERE 
--article_id = 5 
--AND 
--actual_flag = 'A';

	
	
	
	
	