/**
 * 
 * Это сервис, который общается с РЕСТ - сервером для получения и обновления данных
 * 
 * import { AthorsListDataService } from '../lists/_services/athors-list-data.service';
 *  
 * 
 * (c) A.Golibroda 2019
 * 
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

import { Author } 	from 	'../../_models/author';

// это можно будет убрать - это данные.
import { AUTHORSDATA } from '../../__mock/mock-authorsdata';


@Injectable({
  providedIn: 'root'
})
export class AthorsListDataService {

	constructor() { }
	  
	// пока берем данные из набора "мок"	  
	getGroupAuthorsList(groupId: number): Promise<Author[]> {
		// вот тут надо перебрать все, что придет из базы данных, и подставить всем данным правильные света!!!
		// все, цвета что нужно, находятся в массиве "COLORS" 
		return Promise.resolve(AUTHORSDATA);
	}
	  
		

//		getGroupAuthorsList (groupId: number): Observable<Article[]> {
//		//  куда то надо вставить groupId - что бы выбрать из Реста только группу...
//			return this.http.get<Article[]>(this.listArticleUrl)
//				.pipe(
//					tap(_ => this.log('fetched groups')),
//						catchError(this.handleError('getArticlesList', []))
//				);
//		}

/////////////////////////////////////////////////////////////
	
	// пока берем данные из набора "мок"
	//  по - любому, это - получить полный список авторов.
	getAuthorsList(): Promise<Author[]> {
		// вот тут надо перебрать все, что придет из базы данных, и подставить всем данным правильные света!!!
		// все, цвета что нужно, находятся в массиве "COLORS" 
		return Promise.resolve(AUTHORSDATA);
	}
	
	
	
}
