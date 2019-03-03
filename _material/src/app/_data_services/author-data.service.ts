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

import { HttpClient, HttpHeaders } from '@angular/common/http';

import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

//import { MessageService } from './message.service';
//
//const httpOptions = {
//  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
//};

import { REST_SERVER_URL } from '../_config/main';

import { Author } 	from 	'../_models/author';

//это можно будет убрать - это данные.
import { AUTHORSDATA } from '../__mock/mock-authorsdata';


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

    getAll() {
        return this.http.get<Author[]>(`${REST_SERVER_URL}/authors`);
    }

//    getById(id: number) {
//        return this.http.get(`${REST_SERVER_URL}/authors/${id}`);
//    }
	getById(authorId:number): Promise<Author> {
//		console.log('getById authorId = ' + JSON.stringify(authorId, null, 4));
//		console.log('getById AUTHORSDATA[authorId] = ' + JSON.stringify(AUTHORSDATA[authorId], null, 4));
		// вот тут надо перебрать все, что придет из базы данных, и подставить всем данным правильные света!!!
		// все, цвета что нужно, находятся в массиве "COLORS" 
		return Promise.resolve(AUTHORSDATA[authorId]);
	}

    register(author: Author) {
        return this.http.post(`${REST_SERVER_URL}/authors/register`, author);
    }

    update(author: Author) {
        return this.http.put(`${REST_SERVER_URL}/authors/${author.id}`, author);
    }  
    
    
    public get currentAuthorValue(): Author {
        return this.currentAuthorSubject.value;
    }
    
    login(authorname: string, password: string) {
        return this.http.post<any>(`${config.apiUrl}/authors/authenticate`, { authorname, password })
            .pipe(map(author => {
                // login successful if there's a jwt token in the response
                if (author && author.token) {
                    // store author details and jwt token in local storage to keep author logged in between page refreshes
                    localStorage.setItem('currentAuthor', JSON.stringify(author));
                    this.currentAuthorSubject.next(author);
                }

                return author;
            }));
    }

    logout() {
        // remove author from local storage to log author out
        localStorage.removeItem('currentAuthor');
        this.currentAuthorSubject.next(null);
    }    
  
}
