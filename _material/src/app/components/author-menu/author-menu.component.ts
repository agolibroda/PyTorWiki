/**
 * author-menu
 * 
 * Реализовать кусочек меню - что бы пока нет логина был логин, 
 * а после логина - или логоут или редактирование профиля 
 * 
 * import { AuthorMenuComponent } from '../author-menu/author-menu.component';
 *
 * 
 * (c) A.Golibroda 2019
 * 
*/


import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-author-menu',
  templateUrl: './author-menu.component.html',
  styleUrls: ['./author-menu.component.scss']
})
export class AuthorMenuComponent implements OnInit {

  constructor() { }

  ngOnInit() {

//      localStorage.setItem('_currentAuthor', JSON.stringify(_author));
      let _author = JSON.parse(localStorage.getItem('lsCurrentAuthor'));
		console.log('getGroup _author = ' + JSON.stringify(_author, null, 4));
      if (_author && _author.dt_header_id) {
// вот теперь можно подумать о том, как в меню добавить новые пкнктики.
    	  console.log('getGroup _author = ' + JSON.stringify(_author, null, 4));
    	  
      }

		
  }

}
