import { Component} from '@angular/core';

import { Title, Meta }     from '@angular/platform-browser';

import { HelpersService } from './_data_services/helpers.service';


import { environment } from './../environments/environment';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {
	// this.siteTitle:string="Vedogon";
	private _titleService: Title;
	private _metaService: Meta;

	
	public getTitle() : Title {
		return this._titleService;
	}

	public setTitle(v : Title) {
		this._titleService = v;
	}
	
	

	public constructor( private helpers: HelpersService ) { 

		// __dirname +
		// console.log(   " environment = %s", JSON.stringify(environment, null, '\t') );

		// Conversion of type 'string' to type 'Title' may be a mistake 
		// because neither type sufficiently overlaps with the other. If this was intentional, 
		// convert the expression to 'unknown' first.ts(2352)

		this.setTitle(<Title>environment.title);
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
	  
	//   this.titleService.setTitle( environment.title );
	  
}
