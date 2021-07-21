import { Component, OnInit } from '@angular/core';

import { REST_SERVER_URL, MAIN_SITE_TITLE, MAIN_MENU } 			from '../../_config/main';

declare const $: any;
declare interface RouteInfo {
    path: string;
    title: string;
    icon: string;
    class: string;
}
export const ROUTES: RouteInfo[] = [
    { path: MAIN_MENU.groups.path, 		title: MAIN_MENU.groups.title,  icon: MAIN_MENU.groups.icon, class: '' },
    { path: MAIN_MENU.authors.path, 	title: MAIN_MENU.authors.title,  icon: MAIN_MENU.authors.icon, class: '' },
    { path: MAIN_MENU.newArticle.path, 	title: MAIN_MENU.newArticle.title, icon: MAIN_MENU.newArticle.icon, class: '' },
    { path: MAIN_MENU.newGroup.path, 		title: MAIN_MENU.newGroup.title,  icon: MAIN_MENU.newGroup.icon, class: '' },
    
];

// export const MainSiteTitle = MAIN_SITE_TITLE;



@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})

export class SidebarComponent implements OnInit {
  menuItems: any[];
  mainSiteTitle: string;

  constructor() { }

  // вот тут происходит наполнение меню пунктами!
  
  ngOnInit() {
    this.menuItems = ROUTES.filter(menuItem => menuItem);
    this.mainSiteTitle = MAIN_SITE_TITLE;
  }
  isMobileMenu() {
      if ($(window).width() > 991) {
          return false;
      }
      return true;
  };
}
