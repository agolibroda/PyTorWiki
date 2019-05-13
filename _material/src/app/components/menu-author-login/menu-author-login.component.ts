/**
 * menu-author-login
 * 
 * Реализовать кусочек меню - что бы пока нет логина был логин, 
 * а после логина - или логоут или редактирование профиля 
 * 
 * import { MenuAuthorLoginComponent } from '../menu-author-login/menu-author-login.component';
 *
 * 
 * (c) A.Golibroda 2019
 * 
*/


import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-menu-author-login',
  templateUrl: './menu-author-login.component.html',
  styleUrls: ['./menu-author-login.component.scss']
})
export class MenuAuthorLoginComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
