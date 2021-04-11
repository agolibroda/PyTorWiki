/**
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

import { Group } from '../../_models/group';



// это можно будет убрать - это данные.
import { GROUPDATA } from '../../__mock/mock-groupdata';



@Injectable({
  providedIn: 'root'
})


export class GroupListDataService {

	private listGroupUrl = 'rest/group/list';  // URL to web api
	
	
	constructor() { }
  
  
	getGroupsList(): Promise<Group[]> {
		// вот тут надо перебрать все, что придет из базы данных, и подставить всем данным правильные света!!!
		// все, цвета что нужно, находятся в массиве "COLORS" 
		return Promise.resolve(GROUPDATA);
	}
  
	
	getAuthorGroupsList(authorId): Promise<Group[]> {
		// вот тут надо перебрать все, что придет из базы данных, и подставить всем данным правильные света!!!
		// все, цвета что нужно, находятся в массиве "COLORS" 
		return Promise.resolve(GROUPDATA);
	}
	

//	getGroupsList (): Observable<Group[]> {
//		return this.http.get<Group[]>(this.listGroupUrl)
//			.pipe(
//				tap(_ => this.log('fetched groups')),
//					catchError(this.handleError('getGroupsList', []))
//			);
//	}
  
  
}
