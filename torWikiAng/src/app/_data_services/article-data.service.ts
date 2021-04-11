/**
 * 
 * Это сервис, который общается с РЕСТ - сервером для получения и обновления данных
 * 
 * import { ArticleDataService } from '../_data_services/article-data.service';
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

import { Article } from '../_models/article';

@Injectable({
  providedIn: 'root'
})
export class ArticleDataService {

	
    private currentArticleSubject: BehaviorSubject<Article>;
    public currentArticle: Observable<Article>;
  

    constructor(private http: HttpClient) { 
        this.currentArticleSubject = new BehaviorSubject<Article>(JSON.parse(localStorage.getItem('currentArticle')));
        this.currentArticle = this.currentArticleSubject.asObservable();
    }
    
    public getAll() {
        return this.http.get<Article[]>(`${REST_SERVER_URL}/rest/articles`);
    }
    
    
    public getArticleInGroup(groupId) {
        return this.http.get<Article[]>(`${REST_SERVER_URL}/rest/articles?groupId=${groupId}`);
    }
    
    
    
    public getByTitle(articleTitle) {
        return this.http.get<Article>(`${REST_SERVER_URL}/rest/articles/${articleTitle}`);
    }
    
}
