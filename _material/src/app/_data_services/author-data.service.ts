/**
 * 
 * Это сервис, который общается с РЕСТ - сервером для получения и обновления данных
 * 
 * import { AuthorDataService } from '../_data_services/author-data.service';
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


@Injectable({
  providedIn: 'root'
})

export class AuthorDataService {
	
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
        return this.http.get<Author[]>(`${REST_SERVER_URL}/rest/authors`);
    }

    // delete $http.defaults.headers.common['X-Requested-With'];
    
    getById(id: number): Observable<Author> {
		console.log('AuthorDataService::: getById id = ' + JSON.stringify(id, null, 4));
        return this.http.get<Author>(`${REST_SERVER_URL}/rest/authors/${id}`)
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
		
//		this.http.get(`${REST_SERVER_URL}/rest/authors/${id}`)
//		.then(function(response) {
////            $scope.categoriess = response.data;        
//            console.log(response.data);
//        }, function(error) {});		
		
//		как правильно вызвать рест сервис в ангуларе?
//        return this.getDataObservable(`${REST_SERVER_URL}/rest/authors/${id}`)
//        		.subscribe(
//                data => {
////                		this.currentAuthor = <Author>data ;
//                          console.log("I SEE DATA HERE: ", data);
////                          return this.currentAuthor
//                         }
//            );        
//    }
    
//    public getById(authorId:number): Promise<Author> {
////		console.log('getById authorId = ' + JSON.stringify(authorId, null, 4));
////		console.log('getById AUTHORSDATA[authorId] = ' + JSON.stringify(AUTHORSDATA[authorId], null, 4));
//		// вот тут надо перебрать все, что придет из базы данных, и подставить всем данным правильные света!!!
//		// все, цвета что нужно, находятся в массиве "COLORS" 
//		return Promise.resolve(AUTHORSDATA[authorId]);
//	}

    
//    /rest/authors?groupId=123
    //  of authorsGroupList
    /**
     * Получить список всех Авторов, которые участвуют в группе
     */
    getAuthorsInGroup(idGroup: number): Observable<Author> {
		console.log('AuthorDataService::: getAuthorsInGroup idGroup = ' + JSON.stringify(idGroup, null, 4));
        return this.http.get<Author>(`${REST_SERVER_URL}/rest/authors?groupId=${idGroup}`)
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
    
    
    
////////////////////////////////////////////////////////////////////////////
    
    
    public get currentAuthorValue(): Author {
        return this.currentAuthorSubject.value;
    }

    public register(author: Author) {
        return this.http.post(`${REST_SERVER_URL}/rest/authors/register`, author);
    }

    public update(author: Author) {
        return this.http.put(`${REST_SERVER_URL}/rest/authors/${author.dt_header_id}`, author);
    }  
    
    public login(authorname: string, password: string, saveMe: boolean, tag: string) {
        return this.http.post<any>(`${REST_SERVER_URL}/rest/login`, { authorname: authorname, password: password, saveMe: saveMe, tag: tag })
            .pipe(map(_author => {
                //login successful if there's a jwt token in the response
            	console.log('login::: _author = ' + JSON.stringify(_author, null, 4));
            	
                if (_author) {
                    // store author details and jwt token in local storage to keep author logged in between page refreshes
                    localStorage.setItem('lsCurrentAuthor', JSON.stringify(_author));
                }

                return _author;
            }));
    }

    public logout(tag: string) {
        // remove author from local storage to log author out
    	console.log('logout::: tag = ' + JSON.stringify(tag, null, 4));
        return this.http.post<any>(`${REST_SERVER_URL}/rest/logout`, { tag: tag })
        .pipe(map(() => {
            localStorage.removeItem('lsCurrentAuthor');
            localStorage.removeItem('token');
            return true;
        }));
    }    
  
}
