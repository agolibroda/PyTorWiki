/**
 * Визуальный элемент - список Авторов - просто список  
 * как раз тут будем делать всякие украшательства списка тумбочек :-)  
 * 
 * (c) A.Golibroda 2019
 * 
 */


import { Component, OnInit } from '@angular/core';

import { Author } from '../_models/author';
import { AuthorDataService } 		from '../_data_services/author-data.service';


import { MAIN_COLOR, COLORS, ColorSelector } from '../_config/colors';


@Component({
  selector: 'app-authors',
  templateUrl: './authors.component.html',
  styleUrls: ['./authors.component.css']
})

export class AuthorsComponent implements OnInit {

	authorsList: Author[];
	itemColor: ColorSelector;

constructor(
		private authorDataService: AuthorDataService
		) { 
	this.itemColor = new ColorSelector();
}

/**
 * При старте формочки "просмотр списка групп"
 * 
 *  Происходят следующие везчи:
 *  - выбираем первую страницу глобального списка групп. 
 * 
 * 
 */
ngOnInit(): void {
	
	this.authorDataService.getAll()
	.subscribe(authorsList => {
		// вот тут нужно перебрать все элементы списка групп, а в каждую всунуть цвет, который стоит взять из
		// списка цветов, о которых знает система.
		this.authorsList = authorsList.map((group) => {
			group.color = this.itemColor.get();//'primary';
			return group;
		});
		
		return this.authorsList;
	});
}

}
