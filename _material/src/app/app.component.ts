import { Component} from '@angular/core';

import { Title, Meta }     from '@angular/platform-browser';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
	// this.siteTitle:string="Vedogon";
	private titleService: Title;
	private metaService: Meta;

	 public constructor( ) { 
//		 this.titleService.setTitle( "Vedogon" );
//		 this.metaService.addTag({[prop: "description"]: "Что - то супер-пупер!"});
//		 и вообще, стоит поискать примеры использования метатегов !!!!
		 
		 
	 }

//	  public setTitle( newTitle: string) {
//	    this.titleService.setTitle( newTitle );
//	  }
	  
	  
//	  setTitle( 'Good afternoon!' );
	  
//	  this.titleService.setTitle( "Vedogon" );
	  
}
