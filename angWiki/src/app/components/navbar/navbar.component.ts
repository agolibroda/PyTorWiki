/**
 * 
 * 
 * 
 * import { NavbarComponent } from '../components/navbar/navbar.component';
 * 
 */


import { Component, OnInit, ElementRef } from '@angular/core';
import { ROUTES } from '../sidebar/sidebar.component';

//import { LoginComponent }     from '../../login/login.component';
//import { LogoutComponent }    from '../../logout/logout.component'; // logout

import { AuthorDataService } from '../../_data_services/author-data.service';

import { Author } from '../../_models/author';

//import * as myGlobals from '../../globals';
//import { globals } from '../../globals';



import {Location, LocationStrategy, PathLocationStrategy} from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})

export class NavbarComponent implements OnInit {
  private listTitles: any[];
  private mobile_menu_visible: any = 0;
  private toggleButton: any;
  private sidebarVisible: boolean;
	private authorProfile: Author; // Автор
  private isLogin: boolean; // 
  private isProfile: boolean; // 

    constructor(
              private authorDataService: AuthorDataService,
              private location: Location, 
              private element: ElementRef, 
              private router: Router
              ) {
        this.location = location;
        this.sidebarVisible = false;
        this.authorDataService.isLogin$.subscribe(value => this.setIsLogin(value));
        
    }

    ngOnInit(){
      
      this.listTitles = ROUTES.filter(listTitle => listTitle);
      const navbar: HTMLElement = this.element.nativeElement;
      this.toggleButton = navbar.getElementsByClassName('navbar-toggler')[0];
      this.router.events.subscribe((event) => {
        this.sidebarClose();
         var $layer: any = document.getElementsByClassName('close-layer')[0];
         if ($layer) {
           $layer.remove();
           this.mobile_menu_visible = 0;
         }
     });
      
		this.authorProfile = JSON.parse(localStorage.getItem('lsCurrentAuthor'));
		this.isLogin = (this.authorProfile && this.authorProfile.hasOwnProperty('dt_header_id') 
				&& +this.authorProfile.dt_header_id > 0);
		this.isProfile = this.authorProfile && this.authorProfile.hasOwnProperty('dt_header_id') 
				&& +this.authorProfile.dt_header_id > 0;
				
	      console.log('NavbarComponent ::: ngOnInit this.authorProfile = ' + this.authorProfile);
	      console.log('NavbarComponent ::: setIsLogin isLogin = ' + this.isLogin);
	      
				
    }

    setIsLogin(value) {
      console.log('NavbarComponent ::: setIsLogin value = ' + value);
      
      this.isLogin = value !== null;
      this.isProfile = value !== null;
      
      this.authorProfile = value;
      
      console.log('NavbarComponent ::: setIsLogin authorProfile = ' + this.authorProfile);
      console.log('NavbarComponent ::: setIsLogin isLogin = ' + this.isLogin);

    }
    
    sidebarOpen() {
        const toggleButton = this.toggleButton;
        const body = document.getElementsByTagName('body')[0];
        setTimeout(function(){
            toggleButton.classList.add('toggled');
        }, 500);

        body.classList.add('nav-open');

        this.sidebarVisible = true;
    };
    sidebarClose() {
        const body = document.getElementsByTagName('body')[0];
        this.toggleButton.classList.remove('toggled');
        this.sidebarVisible = false;
        body.classList.remove('nav-open');
    };
    sidebarToggle() {
        // const toggleButton = this.toggleButton;
        // const body = document.getElementsByTagName('body')[0];
        var $toggle = document.getElementsByClassName('navbar-toggler')[0];

        if (this.sidebarVisible === false) {
            this.sidebarOpen();
        } else {
            this.sidebarClose();
        }
        const body = document.getElementsByTagName('body')[0];

        if (this.mobile_menu_visible == 1) {
            // $('html').removeClass('nav-open');
            body.classList.remove('nav-open');
            if ($layer) {
                $layer.remove();
            }
            setTimeout(function() {
                $toggle.classList.remove('toggled');
            }, 400);

            this.mobile_menu_visible = 0;
        } else {
            setTimeout(function() {
                $toggle.classList.add('toggled');
            }, 430);

            var $layer = document.createElement('div');
            $layer.setAttribute('class', 'close-layer');


            if (body.querySelectorAll('.main-panel')) {
                document.getElementsByClassName('main-panel')[0].appendChild($layer);
            }else if (body.classList.contains('off-canvas-sidebar')) {
                document.getElementsByClassName('wrapper-full-page')[0].appendChild($layer);
            }

            setTimeout(function() {
                $layer.classList.add('visible');
            }, 100);

            $layer.onclick = function() { //asign a function
              body.classList.remove('nav-open');
              this.mobile_menu_visible = 0;
              $layer.classList.remove('visible');
              setTimeout(function() {
                  $layer.remove();
                  $toggle.classList.remove('toggled');
              }, 400);
            }.bind(this);

            body.classList.add('nav-open');
            this.mobile_menu_visible = 1;

        }
    };

    getTitle(){
      var titlee = this.location.prepareExternalUrl(this.location.path());
      if(titlee.charAt(0) === '#'){
          titlee = titlee.slice( 2 );
      }
      titlee = titlee.split('/').pop();

      for(var item = 0; item < this.listTitles.length; item++){
          if(this.listTitles[item].path === titlee){
              return this.listTitles[item].title;
          }
      }
      return 'Groups';
    }
}