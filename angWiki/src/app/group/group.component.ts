/**
 * Витрина, и редактор (??)
 * 
 * Группы 
 * 
 * (c) A.Golibroda 2019
 * 
 */


import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
//import { Location } from '@angular/common';


import { Group } 	from 	'../_models/group';
import { Article } 	from 	'../_models/article';
import { Author } 	from 	'../_models/author';

import { GroupDataService } from '../_data_services/group-data.service';

//import { ArticlesListDataService } from '../_data_services/lists/article-list-data.service';
//import { AthorsListDataService } from '../_data_services/lists/athors-list-data.service';

import { AuthorDataService } 	from '../_data_services/author-data.service';
import { ArticleDataService } 	from '../_data_services/article-data.service';


import { MAIN_COLOR, COLORS, ColorSelector } from '../_config/colors';

@Component({
  selector: 'app-group',
  templateUrl: './group.component.html',
  styleUrls: ['./group.component.css']
})
export class GroupComponent implements OnInit {

//	route:
	
	groupData: Group; // описание группы (заголовок)
	articlesList: Article[]; // список статей
	authorsList: Author[]; // список Авторов

	itemColor: ColorSelector;

//	groupDataService: GroupDataService;
//	articlesListDataService: ArticleDataService;
//	authorsListDataService: AuthorDataService;

	constructor(
			private groupDataService: GroupDataService,
			private readonly route: ActivatedRoute,
		    private articleDataService: ArticleDataService,
		    private authorsListDataService: AuthorDataService,
		    private readonly router: Router,
		  ) {		
		
		this.itemColor = new ColorSelector();
		
	}
		

	ngOnInit(): void {
		let testId = +this.route.snapshot.paramMap.get("id");
//		console.log('ngOnInit testId = ' + JSON.stringify(testId, null, 4));
		
		this.getGroup(testId);
	}
	
	/**
	 *  "просмотр описания группы"
	 * 
	 *  Происходят следующие везчи:
	 *   - выбрать надо описание группы (по номеру группы, естественно!)
	 *   - выбрать весь (или первую страницу?) списка статей, которых есть в группе 
	 *   - выбрать первую страницу Авторов, которые состоят в Группе.
	 * 
	 * 
	 */
	getGroup(groupId: number): void {
		// public groupId: number
		console.log('getGroup groupId = ' + JSON.stringify(groupId, null, 4));

		if (groupId > 0) {
			this.groupDataService.getById(groupId)
			.subscribe((_groupData: Group) => {
				console.log('getGroup _groupData = ' + JSON.stringify(_groupData, null, 4));
				// Заберем описание группы
				this.groupData = _groupData;
				// А вот теперь надо добавить список статей в группе  
				// и список авторов!!!!!
				
				this.articleDataService.getArticleInGroup(groupId)
				.subscribe((_articlesList: Article[]) => {
					// вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
					// списка цветов, о которых знает система.
					this.articlesList = _articlesList.map((article) => {
						article.color = this.itemColor.get();//'primary';
						return article;
					});
					
//							console.log('AuthorViewComponent::: getAuthor this.articlesList = ' + JSON.stringify(this.articlesList, null, 4));
					// Заберем всех АВТОРОВ этой группы!!!!!!
					this.authorsListDataService.getAuthorsInGroup(groupId)
//							.subscribe((_authorsList: Author[]) => {
//								// вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
//								// списка цветов, о которых знает система.
//								this.authorsList = _authorsList.map((author) => {
//									author.color = this.itemColor.get();//'primary';
//									return author;
//								});
//							})
				})
				
			})
			
		} else {
			// тут надо перейти к редактированию новой группы
			this.groupData = new Group();
			this.articlesList = [];
			this.authorsList = [];
		}
		
	}
	
	
	// 
}
