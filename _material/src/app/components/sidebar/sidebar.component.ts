import { Component, OnInit } from '@angular/core';

import { REST_SERVER_URL, MAIN_MENU } 			from '../../_config/main';

declare const $: any;
declare interface RouteInfo {
    path: string;
    title: string;
    icon: string;
    class: string;
}
export const ROUTES: RouteInfo[] = [
    { path: '/groups', 		title: MAIN_MENU.groups.title,  icon: MAIN_MENU.groups.icon, class: '' },
    { path: '/authors', 	title: MAIN_MENU.authors.title,  icon: MAIN_MENU.authors.icon, class: '' },
    { path: '/author-profile', 	title: 'User Profile(убрать!)',  icon:'person', class: '' },
    { path: '/article', 	title: MAIN_MENU.newArticle.title, icon: MAIN_MENU.newArticle.icon, class: '' },
    { path: '/group', 		title: MAIN_MENU.newGroup.title,  icon: MAIN_MENU.newGroup.icon, class: '' },
    
];

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  menuItems: any[];

  constructor() { }

  // вот тут происходит наполнение меню пунктами!
  
  ngOnInit() {
    this.menuItems = ROUTES.filter(menuItem => menuItem);
  }
  isMobileMenu() {
      if ($(window).width() > 991) {
          return false;
      }
      return true;
  };
}
