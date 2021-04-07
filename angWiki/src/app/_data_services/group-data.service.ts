/**
 * 
 * Это сервис, который общается с РЕСТ - сервером для получения и обновления данных
 * 
 * import { GroupDataService } from '../_data_services/group-data.service';

 *  
 * 
 * (c) A.Golibroda 2019
 * 
 */



import { Injectable } from '@angular/core';

import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { first } from 'rxjs/operators';

import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

//import { MessageService } from './message.service';

import { REST_SERVER_URL } from '../_config/main';

import { Author } 	from 	'../_models/author';
import { Group } from '../_models/group';



@Injectable({
  providedIn: 'root'
})
export class GroupDataService {

    private currentAuthorSubject: BehaviorSubject<Author>;
    public currentAuthor: Observable<Author>;
  

    constructor(private http: HttpClient) { 
        this.currentAuthorSubject = new BehaviorSubject<Author>(JSON.parse(localStorage.getItem('currentAuthor')));
        this.currentAuthor = this.currentAuthorSubject.asObservable();
    }
    
    
    getDataObservable(url:string) {
        return this.http.get(url)
//            .map(data => {
//                data.json();
//                // the console.log(...) line prevents your code from working 
//                // either remove it or add the line below (return ...)
//                console.log("I CAN SEE DATA HERE: ", data.json());
//                return data.json();
//        });
    }    

    
    public handleError(error: HttpErrorResponse) {
    	  if (error.error instanceof ErrorEvent) {
    	    // A client-side or network error occurred. Handle it accordingly.
    	    console.error('An error occurred:', error.error.message);
    	  } else {
    	    // The backend returned an unsuccessful response code.
    	    // The response body may contain clues as to what went wrong,
    	    console.error(
    	      `Backend returned code ${error.status}, ` +
    	      `body was: ${error.error}`);
    	  }
    	  // return an observable with a user-facing error message
    	  return throwError(
    	    'Something bad happened; please try again later.');
    	};
    
    public getAll() {
        return this.http.get<Group[]>(`${REST_SERVER_URL}/rest/groups`);
    }

    // delete $http.defaults.headers.common['X-Requested-With'];
    
    getById(id: number): Observable<Group> {
//		console.log('GroupDataService::: getById id = ' + JSON.stringify(id, null, 4));
        return this.http.get<Group>(`${REST_SERVER_URL}/rest/groups/${id}`)
//        			.pipe(catchError(this.handleError) )
//        			.pipe(first())
//        			.then(_authorData => {
//        				console.log('GroupDataService::: getById _authorData = ' + JSON.stringify(_authorData, null, 4));
//        				return _authorData;
//        			});

//		.subscribe((response:Group) => {
//			console.log('GroupDataService::: response = ' + JSON.stringify(response, null, 4));
////			this.currentAuthor=response;
//			return response
//			});
		}
  
    /**
     * Получить список всех групп, в которых участвует автор
     */
    getAuthorGroups(authorId: number): Observable<Author> {
		console.log('AuthorDataService::: getAuthorGroups authorId = ' + JSON.stringify(authorId, null, 4));
        return this.http.get<Author>(`${REST_SERVER_URL}/rest/groups?authorId=${authorId}`)
//        			.pipe(catchError(this.handleError) )
//        			.pipe(first())
//        			.then(_authorData => {
//        				console.log('AuthorDataService::: getById _authorData = ' + JSON.stringify(_authorData, null, 4));
//        				return _authorData;
//        			});

//		.subscribe((response:Author) => {
//			console.log('AuthorDataService::: response = ' + JSON.stringify(response, null, 4));
////			this.currentAuthor=response;
//			return response
//			});
		}    
    
  
}
