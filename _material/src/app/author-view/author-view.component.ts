/**
 * Витрина пользователя
 * 
 * (c) A.Golibroda 2019
 * 
 */


import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { MAIN_COLOR, COLORS, ColorSelector } from '../_config/colors';

import { Group } 	from 	'../_models/group';
import { Article } 	from 	'../_models/article';
import { Author } 	from 	'../_models/author';

import { AuthorDataService } 		from '../_data_services/author-data.service';
import { ArticlesListDataService } 	from '../lists/_services/article-list-data.service';
import { GroupListDataService } 	from '../lists/_services/group-list-data.service';


@Component({
  selector: 'app-author-view',
  templateUrl: './author-view.component.html',
  styleUrls: ['./author-view.component.scss']
})
export class AuthorViewComponent implements OnInit {

	authorData: Author; // описание Автора (заголовок)
	articlesList: Article[]; // список статей
	groupsList: Group[]; // список групп, в которых Автор участник

	itemColor: ColorSelector;

	authorDataService: AuthorDataService;
	articlesListDataService: ArticlesListDataService;
	groupsListDataService: GroupListDataService;
	
	courseId: number;

//constructor( private route: ActivatedRoute, private location: Location) { 
	constructor(
		    private readonly route: ActivatedRoute,
		    private readonly router: Router,
		  ) {		
		
		this.itemColor = new ColorSelector();

		this.authorDataService = new AuthorDataService();

		this.articlesListDataService = new ArticlesListDataService();
	
		this.groupsListDataService = new GroupListDataService();

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
		
		this.getAuthor(testId);
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
	getAuthor(authorId: number): void {
		// public authorId: number
//				console.log('getAuthor authorId = ' + JSON.stringify(authorId, null, 4));

				if (authorId > 0) {
					this.authorDataService.getById(authorId)
					.then(_authorData => {
						// Заберем описание Автора
						this.authorData = _authorData
						console.log('this.authorData = ' + JSON.stringify(this.authorData, null, 4));
						// Заберем список статей, Автора
						return this.articlesListDataService.getArticlesAutorList(authorId);
					}).then(_articlesList => {
						// вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
						// списка цветов, о которых знает система.
						this.articlesList = _articlesList.map((article) => {
							article.color = this.itemColor.get();//'primary';
							return article;
						});
						// Заберем все группы автора
						return this.groupsListDataService.getAuthorGroupsList(authorId);
					})
					.then(_groupsList => {
						// вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
						// списка цветов, о которых знает система.
						this.groupsList = _groupsList.map((group) => {
							group.color = this.itemColor.get();
							return group;
						});
						
//						this.groupsList = this.itemColor.setColors(_groupsList);
						// положим авторов "куда надо"
					});
					
				} else {
					// тут надо перейти к редактированию новой группы
					this.authorData = new Author();
					this.articlesList = [];
					this.groupsList = [];
				}
				
			}

}
