import { Component} from '@angular/core';

import { Title, Meta }     from '@angular/platform-browser';

import { HelpersService } from './_data_services/helpers.service';




@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
	// this.siteTitle:string="Vedogon";
	private titleService: Title;
	private metaService: Meta;

	

	 public constructor( private helpers: HelpersService ) { 
//		 this.titleService.setTitle( "Vedogon" );
//		 this.metaService.addTag({[prop: "description"]: "Что - то супер-пупер!"});
//		 и вообще, стоит поискать примеры использования метатегов !!!!
		 
		 let token = <string>localStorage.getItem('token');
//		 console.log('AppComponent::: 1 token = ' + JSON.stringify(token, null, 4));
		 
		 if (token) {
			 this.helpers.checkToken(token)
			 .subscribe((_rezult) => {
//				console.log('AppComponent::: _rezult = ' + JSON.stringify(_rezult, null, 4));
				if (!_rezult) {
					token = '';
					localStorage.removeItem('token');
					// и все остальные данные, относящиеся к персоне - автору.
					
					//  а потом сделать новый токен
					this.helpers.getToken()
					.subscribe((_token) => {
		 				localStorage.setItem('token', <string>_token);
		 			});
				}
			})
		 }
		 
		 if ( !token ) {
			 this.helpers.getToken()
			 .subscribe((_token) => {
				localStorage.setItem('token', <string>_token);
			 });
		 } 
	 }

//	  public setTitle( newTitle: string) {
//	    this.titleService.setTitle( newTitle );
//	  }
	  
	  
//	  setTitle( 'Good afternoon!' );
	  
//	  this.titleService.setTitle( "Vedogon" );
	  
}
