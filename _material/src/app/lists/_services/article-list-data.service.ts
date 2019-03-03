/**
 * article.ts
 * 
 * Получить список статей для чего? по поводу?
 * - для Автора (все статьи в написании которых Автор отметился )
 * - для группы все статьи, которые включены в группу
 * - все статьи, которые были найдены (отфильтрованы)  
 * 
 * import { ArticleListDataService } from '../lists/_services/article-list-data.service';
 * 
 * 
 * (c) A.Golibroda 2019
 */


import { Injectable } from '@angular/core';

import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

//import { MessageService } from './message.service';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

import { REST_SERVER_URL } from '../../_config/main';

import { Article } from '../../_models/article';



// это можно будет убрать - это данные.
import { ARTICLEDATA } from '../../__mock/mock-articledata';


@Injectable({
  providedIn: 'root'
})


export class ArticlesListDataService {

	constructor() { }
	  
// пока берем данные из набора "мок"	  
	getArticlesGroupList(groupId: number): Promise<Article[]> {
		// вот тут надо перебрать все, что придет из базы данных, и подставить всем данным правильные света!!!
		// все, цвета что нужно, находятся в массиве "COLORS" 
		return Promise.resolve(ARTICLEDATA);
	}
  
	getArticlesAutorList(authorId: number): Promise<Article[]> {
		// вот тут надо перебрать все, что придет из базы данных, и подставить всем данным правильные света!!!
		// все, цвета что нужно, находятся в массиве "COLORS" 
		return Promise.resolve(ARTICLEDATA);
	}
	

//	getArticlesGroupList (groupId: number): Observable<Article[]> {
//	//  куда то надо вставить groupId - что бы выбрать из Рестра только группу...
//		return this.http.get<Article[]>(this.listArticleUrl)
//			.pipe(
//				tap(_ => this.log('fetched groups')),
//					catchError(this.handleError('getArticlesList', []))
//			);
//	}
  
}
