/**
 * 
 * Это сервис, Для всякой всячины, в частности, для получения ТОкена
 *  РЕСТ 
 * 
 * import { HelpersService } from '../_data_services/helpers.service';
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
export class HelpersService {

  constructor(private http: HttpClient) { }
  
  
  
  public getToken() {
      return this.http.get(`${REST_SERVER_URL}/rest/token`);
  }
  

  public checkToken(token) {
      return this.http.get(`${REST_SERVER_URL}/rest/check_token/${token}`);
  }

  
  
}
