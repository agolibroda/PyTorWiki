import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { first } from 'rxjs/operators';
import { catchError, retry } from 'rxjs/operators';


import { MAIN_COLOR, COLORS, ColorSelector } from '../_config/colors';

import { Group } 	from 	'../_models/group';
import { Article } 	from 	'../_models/article';
import { Author } 	from 	'../_models/author';

import { AuthorDataService } 		from '../_data_services/author-data.service';
import { ArticlesListDataService } 	from '../_data_services/lists/article-list-data.service';
import { GroupListDataService } 	from '../_data_services/lists/group-list-data.service';


@Component({
  selector: 'app-author-profile',
  templateUrl: './author-profile.component.html',
  styleUrls: ['./author-profile.component.css']
})

export class AuthorProfileComponent implements OnInit {

//	currentAuthorSubscription: Subscription;

	currentAuthor: Author; // описание Автора (заголовок)
	currentAuthorSubscription: Subscription;
	articlesList: Article[]; // список статей
	groupsList: Group[]; // список групп, в которых Автор участник
	
	itemColor: ColorSelector;
	
//	authorDataService: AuthorDataService;
	articlesListDataService: ArticlesListDataService;
	groupsListDataService: GroupListDataService;
	
	courseId: number;
	
	constructor(
			private authorDataService: AuthorDataService,
			private route: ActivatedRoute,
			private router: Router,
		     
		  ) {		
		
		this.itemColor = new ColorSelector();
		
		this.authorProfile = new Author();
		this.articlesList = [];
		this.groupsList = [];
	
//		this.authorDataService = new AuthorDataService();
	
		this.articlesListDataService = new ArticlesListDataService();
	
		this.groupsListDataService = new GroupListDataService();
	
//		this.currentAuthorSubscription = this.authorDataService.currentAuthor.subscribe(_author => {
//			this.currentAuthor = _author;
//		});
// 		console.log('AuthorProfileComponent:: constructor this.currentAuthor = ' + JSON.stringify(this.currentAuthor, null, 4));
	}
	
	
	ngOnInit(): void {
		// вот тут все несколько иначе - 
		// надо выдернуть ИД да и все данные из сессии - из редиски
		// и разместить данные в полях для редактирования.
//		let testId = +this.route.snapshot.paramMap.get("id");
//		console.log('ngOnInit testId = ' + JSON.stringify(testId, null, 4));
//		let testId = 6
		
//		this.getAuthor(testId);
		
		this.authorProfile = JSON.parse(localStorage.getItem('lsCurrentAuthor'));
		
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
			console.log('AuthorProfileComponent getGroup Start!!!  ' );
//			currentAuthor: Author;
			
//			const authorId = 0 ; //+this.route.snapshot.paramMap.get('id');

			console.log('AuthorProfileComponent getAuthor authorId = ' + JSON.stringify(authorId, null, 4));

			if (authorId > 0) {
				this.authorDataService.getById(authorId)
				.pipe(catchError(this.authorDataService.handleError) )
				.subscribe((_currentAuthor: Author) => {
						console.log('AuthorViewComponent::: getAuthor _currentAuthor = ' + JSON.stringify(_currentAuthor, null, 4));
						this.currentAuthor = <Author>_currentAuthor;
						// Заберем список статей, Автора
						this.articlesListDataService.getArticlesAutorList(authorId)
						.then(_articlesList => {
							// вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
							// списка цветов, о которых знает система.
							this.articlesList = _articlesList.map((article) => {
								article.color = this.itemColor.get();//'primary';
								return article;
							});
//							console.log('AuthorViewComponent::: getAuthor this.articlesList = ' + JSON.stringify(this.articlesList, null, 4));
							// Заберем все группы автора
//							return this.groupsListDataService.getAuthorGroupsList(authorId);
						})
						
				})
//		        .catch(err => {
//		        	console.log('getAuthor err = ' + JSON.stringify(err, null, 4));
//                }))
//				.then(_currentAuthor => {
//					// Заберем описание Автора
//					this.currentAuthor = <Author>_currentAuthor
//					console.log('getAuthor this.currentAuthor = ' + JSON.stringify(this.currentAuthor, null, 4));
//					// Заберем список статей, Автора
//					return this.articlesListDataService.getArticlesAutorList(authorId);
//				})
//				.then(_articlesList => {
//					// вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
//					// списка цветов, о которых знает система.
//					this.articlesList = _articlesList.map((article) => {
//						article.color = this.itemColor.get();//'primary';
//						return article;
//					});
//					// Заберем все группы автора
//					return this.groupsListDataService.getAuthorGroupsList(authorId);
//				})
//				.then(_groupsList => {
//					// вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
//					// списка цветов, о которых знает система.
//					this.groupsList = _groupsList.map((group) => {
//						group.color = this.itemColor.get();
//						return group;
//					});
					
//					this.groupsList = this.itemColor.setColors(_groupsList);
					// положим авторов "куда надо"
//				});
				
			} else {
				// тут надо перейти к редактированию новой группы
//				this.currentAuthor = new Author();
//				this.articlesList = [];
//				this.groupsList = [];
			}
			
		}

}
