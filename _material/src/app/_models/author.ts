/**
 * author.ts
 *
 * import { Author } 	from 	'../_models/author';
 * 
 * (c) A.Golibroda 2019
 * 
 */

export class Author {
	
	dt_header_id: number;
	author_login: string;
	author_name: string;
	author_surname: string;
	author_phon: string;
	author_email: string;

	author_yourself_story: string; // story about yourself
//Количество статей, уже существующих в группе
	article_count: number; // Сколько статей написал АУтор, будем подсчитывать при составлении списка афторов. 
	group_count: number; // Количество групп, в которых Автор состоит.

//цвет плашки автора, штука случайная, ее надо выбрать из "конфига" случайным образом (или перебором")
	color: string; 


//	grop_picture: {
//		pic_id: number,
//		file_inside_name: string,
//		file_path: string
//		};
	}
