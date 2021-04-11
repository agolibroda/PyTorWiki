/**
 * menu-author-profile
 * 
 * Реализовать кусочек меню - что бы пока нет логина был логин, 
 * а после логина - или логоут или редактирование профиля 
 * 
 * import { LogoutComponent } 			from '../../logout/logout.component'; // logout
 *
 * 
 * (c) A.Golibroda 2019
 * 
*/


import { Component, OnInit, Output } from '@angular/core';
import { NgForm} from '@angular/forms';
import { Router } from '@angular/router';

import { AuthorDataService } from '../_data_services/author-data.service';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.scss']
})
export class LogoutComponent implements OnInit {

  constructor(
			private authorLoginService: AuthorDataService,
			private router: Router
  			) { 
    
//    this.successfulLogout$ = new EventEmitter<boolean>();
    
  }

  ngOnInit() {
	  // удалить из ЛокалСтореджа данные о теге и о пользователе
	  // сделать запрос на сервер для очистки редиски
	  
		  this.authorLoginService.logout(
		  			localStorage.getItem('token')
		  			)
    	 .subscribe(() => {
    		 // А, вот тут надо перепрыгнуть на какую - то другую страницу!!!!
    		 // и, кстати, надо поменять ленку в шиблоне - с "логина" на мой профиль!!!!
    		 // 	и, кстати, стоит перекинуть на главную. 
    	   
    		 this.router.navigate(['/']);
    	 });
  }

}
