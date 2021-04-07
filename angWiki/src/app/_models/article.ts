/**
 * article.ts
 * 
 * import { Article } from '../_models/article';
 * 
 * (c) A.Golibroda 2019
 */

export class Article {
	
	article_id: number; // ИД стстьи, ну, на всякий случай!
    article_title: string; // Заглавие статьи и, ссылка на статью
    article_annotation: string; //  Это аннотация статьи!!!!!
	article_source: string; //  собственно, Это текст статьи
    article_permissions: string; // уровень видимости статьи - чаще всего - публично 'pbl'

    // цвет плашки, на котором может появиться заголовок статьи
	// штука случайная, ее надо выбрать из "конфига" случайным образом (или перебором") 
	// - для выбора цвета придуман специальный класс "ColorSelector"  и его использование:
	// this.itemColor = new ColorSelector();
	color: string;
	group_count: number; // Количество групп, в которых данная статья пребывает.

//
//	article_picture: {
//		pic_id: number,
//		file_inside_name: string,
//		file_path: string
//		};
	}
