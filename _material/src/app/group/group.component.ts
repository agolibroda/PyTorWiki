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
import { ArticlesListDataService } from '../lists/_services/article-list-data.service';
import { AthorsListDataService } from '../lists/_services/athors-list-data.service';


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

	groupDataService: GroupDataService;
	articlesListDataService: ArticlesListDataService;
	authorsListDataService: AthorsListDataService;

	courseId: number;

//	constructor( private route: ActivatedRoute, private location: Location) { 
	constructor(
		    private readonly route: ActivatedRoute,
		    private readonly router: Router,
		  ) {		
		
		this.itemColor = new ColorSelector();
		
		this.articlesListDataService = new ArticlesListDataService();

		this.authorsListDataService = new AthorsListDataService();

		this.groupDataService = new GroupDataService();
	
		this.route.params.subscribe(
				params =>{
					this.courseId = parseInt(params['id']);
				}
		);
		console.log('constructor this.courseId = ' + JSON.stringify(this.courseId, null, 4));
	}
		

	ngOnInit(): void {
		let testId = +this.route.snapshot.paramMap.get("id");
		console.log('ngOnInit testId = ' + JSON.stringify(testId, null, 4));
		
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
				console.log('getGroup Start!!!  ' );
				
//				const groupId = 0 ; //+this.route.snapshot.paramMap.get('id');

				console.log('getGroup groupId = ' + JSON.stringify(groupId, null, 4));

				if (groupId > 0) {
					this.groupDataService.getGroupData(groupId)
					.then(_groupData => {
						// Заберем описание группы
						this.groupData = _groupData
//						console.log('this.groupData = ' + JSON.stringify(this.groupData, null, 4));
						// Заберем список статей, которые есть в ЭТОЙ группе
						return this.articlesListDataService.getArticlesGroupList(groupId);
					}).then(_articlesList => {
						// вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
						// списка цветов, о которых знает система.
						this.articlesList = _articlesList.map((article) => {
							article.color = this.itemColor.get();//'primary';
							return article;
						});
						// Заберем авторов, которые связаны с группой
						return this.authorsListDataService.getGroupAuthorsList(groupId);
					})
					.then(_authorsList => {
						// вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
						// списка цветов, о которых знает система.
						this.authorsList = _authorsList.map((author) => {
							author.color = this.itemColor.get();
							return author;
						});
						
//						this.authorsList = this.itemColor.setColors(_authorsList);
						// положим авторов "куда надо"
					});
					
				} else {
					// тут надо перейти к редактированию новой группы
					this.groupData = new Group();
					this.articlesList = [];
					this.authorsList = [];
				}
				
			}
	
	
	// 
}
