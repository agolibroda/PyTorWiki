
--  надо добавить в Автора, Группу, Статью ОСНОВНУЮ картинку - то, что будет показываться и как "минитюра"
-- и вообще!!!!!!

ALTER TABLE authors
	ADD COLUMN pic_id int NULL,
	ADD COLUMN author_yourself_story text;
	
 
CREATE INDEX author_pic_id_ind ON authors (pic_id);

ALTER TABLE articles
	ADD COLUMN pic_id int NULL;
 
CREATE INDEX article_pic_id_ind ON authors (pic_id);

ALTER TABLE groups
	ADD COLUMN pic_id int NULL;
 
CREATE INDEX group_pic_id_ind ON authors (pic_id);
