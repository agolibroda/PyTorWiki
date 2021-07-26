-- добрался до изменений... 
-- нуно добавить "флаг публичности" для параметров типа почт и телефон.


ALTER TABLE authors
	ADD COLUMN author_is_publick_contakt boolean false; -- Автор разрешает показывать свои персональные данные (почту и телефон)


-- Добавил работу с диалогами.. 


CREATE TABLE IF NOT EXISTS dialogs (
	dialog_id integer NOT NULL primary key, -- ИД..
	dialog_create timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP, -- дата создания диалога

	dialog_1_author_id integer NOT NULL, 
	dialog_2_author_id integer NOT NULL,

	dialog_public_key bytea NOT NULL,
	dialog_private_key_1_author bytea NOT NULL,
	dialog_private_key_2_author bytea NOT NULL,

	CONSTRAINT dialog_1_author_id_fk FOREIGN KEY (dialog_1_author_id)
        REFERENCES public.dt_headers (dt_header_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
	CONSTRAINT dialog_2_author_id_fk FOREIGN KEY (dialog_2_author_id)
        REFERENCES public.dt_headers (dt_header_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
	CONSTRAINT unique_dialog_uk UNIQUE (dialog_1_author_id, dialog_2_author_id)
	-- надо обязательно проверить, чтобы у нас не случилось 2-х диалогов, где А-Б и Б-А !!!
);
  
ALTER TABLE dialogs
    OWNER to wiki_user;


DROP SEQUENCE IF EXISTS dialogs_id_seq CASCADE;
CREATE SEQUENCE IF NOT EXISTS dialogs_id_seq;

CREATE OR REPLACE FUNCTION trigger_dialogs_before_lns () RETURNS trigger AS $$ 
BEGIN 
      If  NEW.dialog_id = 0 OR NEW.dialog_id IS NULL then 
	      NEW.dialog_id = nextval('dialogs_id_seq');
      end if;

return NEW;
END; 
$$ LANGUAGE  plpgsql;

-- Создание триггера
CREATE TRIGGER author_bi 
BEFORE INSERT ON dialogs FOR EACH ROW 
EXECUTE PROCEDURE trigger_dialogs_before_lns ();

-- теперь понаделаем индесов

CREATE INDEX dialog_id_ind
    ON dialogs USING btree
    (dialog_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX dialog_create_ind
    ON dialogs USING btree
    (dialog_create ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX dialog_1_author_id_ind
    ON dialogs USING btree
    (dialog_1_author_id ASC NULLS LAST)
    TABLESPACE pg_default;	

CREATE INDEX dialog_2_author_id_ind
    ON dialogs USING btree
    (dialog_2_author_id ASC NULLS LAST)
    TABLESPACE pg_default;


--  походу, пожалуй пришло время сделать табличку для Сообщений, 




CREATE TABLE IF NOT EXISTS messages (
	message_id integer NOT NULL primary key, -- ИД..

	dialog_id integer NOT NULL,

	message_create timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP, -- дата создания диалога

	message_to_author_id integer NOT NULL, -- кому пишет
	message_from_author_id integer NOT NULL, -- кто пишет 

	message_answer_to_message_id integer, -- в отет на сообщение..

	message_subject varying(256) NOT NULL, -- тема сообщеия всегда открыта!!!!! 
	message_text bytea NOT NULL, -- текст сообщеия ВСЕГДА закрыт!!!!!

	CONSTRAINT dialog_1_author_id_fk FOREIGN KEY (dialog_id)
        REFERENCES public.dialogs (dialog_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
);
  
ALTER TABLE messages
    OWNER to wiki_user;


CREATE INDEX message_id_ind
    ON messages USING btree
    (message_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX dialog_id_ind
    ON messages USING btree
    (dialog_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX message_create_ind
    ON messages USING btree
    (message_create ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX message_to_author_id_ind
    ON messages USING btree
    (message_to_author_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX message_from_author_id_ind
    ON messages USING btree
    (message_from_author_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX message_answer_to_message_id_ind
    ON messages USING btree
    (message_answer_to_message_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX message_subject_ind
    ON messages USING btree
    (message_subject ASC NULLS LAST)
    TABLESPACE pg_default;
