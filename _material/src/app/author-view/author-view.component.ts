/**
 * Витрина пользователя
 * 
 * (c) A.Golibroda 2019
 * 
 */


import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { first } from 'rxjs/operators';
import { catchError, retry } from 'rxjs/operators';


import { MAIN_COLOR, COLORS, ColorSelector } from '../_config/colors';

import { Group } 	from 	'../_models/group';
import { Article } 	from 	'../_models/article';
import { Author } 	from 	'../_models/author';

import { AuthorDataService } 	from '../_data_services/author-data.service';
import { ArticleDataService } 	from '../_data_services/article-data.service';


//import { ArticlesListDataService } 	from '../_data_services/lists/article-list-data.service';
//import { GroupListDataService } 	from '../_data_services/lists/group-list-data.service';
import { GroupDataService } from '../_data_services/group-data.service';

@Component({
  selector: 'app-author-view',
  templateUrl: './author-view.component.html',
  styleUrls: ['./author-view.component.scss']
})
export class AuthorViewComponent implements OnInit {

	currentAuthor: Author; // описание Автора (заголовок)
	articlesList: Article[]; // список статей
	groupsList: Group[]; // список групп, в которых Автор участник
	currentAuthorSubscription: Subscription;


	itemColor: ColorSelector;

//	private authorDataService: AuthorDataService;
	private articlesListDataService: ArticleDataService;
//	private groupsListDataService: GroupDataService;
	
	courseId: number;

//constructor( private route: ActivatedRoute, private location: Location) { 
	constructor(
			private authorDataService: AuthorDataService,
			private articleDataService: ArticleDataService,
			private groupsDataService: GroupDataService,
	        private route: ActivatedRoute,
	        private router: Router
			
		  ) {		
		
		this.itemColor = new ColorSelector();
		
		
		this.currentAuthor = new Author();
		//  а может вот тут вынимать автора (если есть) из хранилища? 
		// ну и все его данные? 
		this.articlesList = [];
		this.groupsList = [];

//		this.articleDataService = new ArticleDataService();
		
//		this.groupsListDataService = new GroupDataService();
	
		this.currentAuthorSubscription = this.authorDataService.currentAuthor.subscribe(_author => {
			this.currentAuthor = _author;
		});
	}
	

	ngOnInit(): void {
		let testId = +this.route.snapshot.paramMap.get("id");
//		console.log('AuthorViewComponent::: ngOnInit testId = ' + JSON.stringify(testId, null, 4));
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

		if (authorId > 0) {

			this.authorDataService.getById(authorId)
			.pipe(catchError(this.authorDataService.handleError) )
			.subscribe((_currentAuthor: Author) => {
//					console.log('AuthorViewComponent::: getAuthor _currentAuthor = ' + JSON.stringify(_currentAuthor, null, 4));
					this.currentAuthor = <Author>_currentAuthor;
					// Заберем список статей, Автора
//					this.articlesListDataService.getArticlesAutorList(authorId)
					this.articleDataService.getAll()
					.subscribe((_articlesList: Article[]) => {
						// вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
						// списка цветов, о которых знает система.
						this.articlesList = _articlesList.map((article) => {
							article.color = this.itemColor.get();//'primary';
							return article;
						});
//						console.log('AuthorViewComponent::: getAuthor this.articlesList = ' + JSON.stringify(this.articlesList, null, 4));
						// Заберем все группы автора
//						return this.groupsListDataService.getAuthorGroupsList(authorId);
						this.groupsDataService.getAuthorGroups(authorId)
//						.subscribe((_groupsList: Author[]) => {
//							// вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
//							// списка цветов, о которых знает система.
//							this.groupsList = _groupsList.map((group) => {
//								group.color = this.itemColor.get();//'primary';
//								return group;
//							});
//						})
						
					})
					
			})
			
		} else {
			// тут надо перейти к редактированию новой группы
//					this.currentAuthor = new Author();
//					this.articlesList = [];
//					this.groupsList = [];
		}
		
	}

}
