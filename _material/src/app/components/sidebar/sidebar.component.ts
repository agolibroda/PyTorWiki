import { Component, OnInit } from '@angular/core';

declare const $: any;
declare interface RouteInfo {
    path: string;
    title: string;
    icon: string;
    class: string;
}
export const ROUTES: RouteInfo[] = [
    { path: '/groups', title: 'Види і форми дозвілля',  icon: 'dashboard', class: '' },
    { path: '/authors', title: 'Автори',  icon:'group', class: '' },
    { path: '/author-profile', title: 'User Profile(убрать!)',  icon:'person', class: '' },
    { path: '/article', title: 'Нова Стаття',  icon:'tab', class: '' },
    { path: '/group', title: 'Новi: вид або форма дозвілля',  icon:'list_alt', class: '' },
    
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
