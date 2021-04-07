/**
 * group.ts
 * 
 * import { Group } from '../_models/group';
 * 
 * 
 * (c) A.Golibroda 2019
 * 
*/


export class Group {
	group_id: number;
	group_title: string;
	group_annotation: string;

//Количество статей, уже существующих в группе
	article_count: number; 
//цвет групповой плашки, штука случайная, ее надо выбрать из "конфига" случайным образом (или перебором")
	color: string; 

//	grop_picture: {
//		pic_id: number,
//		file_inside_name: string,
//		file_path: string
//		};
	}
