/**
 * menu-author-profile
 * 
 * Реализовать кусочек меню - что бы пока нет логина был логин, 
 * а после логина - или логоут или редактирование профиля 
 * 
 * import { MenuAuthorProfileComponent } from '../menu-author-profile/menu-author-profile.component';
 *
 * 
 * (c) A.Golibroda 2019
 * 
*/


import { Component, OnInit } from '@angular/core';

import { REST_SERVER_URL } 			from '../../_config/main';



declare const $: any;
declare interface RouteInfo {
    path: string;
    title: string;
    icon: string;
    class: string;
}

export const ROUTES: RouteInfo[] = [
	
    { path: '/author-profile', 	title: 'Edit Author Profile', 	icon:'person', 			class: '' },
    { path: '/logout', 			title: 'Logout',  				icon: 'exit_to_app', 	class: '' },
    
];

@Component({
  selector: 'app-menu-author-profile',
  templateUrl: './menu-author-profile.component.html',
  styleUrls: ['./menu-author-profile.component.scss']
})
export class MenuAuthorProfileComponent implements OnInit {
	menuAuthorItems: any[];

	constructor() { }

	ngOnInit() {
		this.menuAuthorItems = ROUTES.filter(menuItem => menuItem);
		this.authorProfile = JSON.parse(localStorage.getItem('lsCurrentAuthor'));

	}
	
	isMobileMenu() {
		if ($(window).width() > 991) {
			return false;
		}
		return true;
	};

}
