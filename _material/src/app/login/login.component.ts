import { Component, OnInit } from '@angular/core';
import { NgForm} from '@angular/forms';

import { AuthorDataService } from '../_data_services/author-data.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

	
	constructor(
			private authorLoginService: AuthorDataService
			) { }

  ngOnInit() {
  }

  
  public makeLogin (formData: NgForm) {

	  console.log(formData.value.username);
	  console.log(formData.value.password);
	  console.log(formData.value.saveMe);
	  console.log(formData);
	  
	  this.authorLoginService.login(
			  			formData.value.username, 
			  			formData.value.password, 
			  			formData.value.saveMe, // если флаг включен, то перца мы запомним на год :-) 
			  			localStorage.getItem('token')
			  			)
		 .subscribe((_afterLoginRezult) => {
			 console.log(_afterLoginRezult);
			 // _afterLoginRezult - Это объект, его надо сериализовать, и положить в локалСторедж.
			 localStorage.setItem('author', <string>_afterLoginRezult);
        			});
	  
//		 this.helpers.makeLogin()
//		 .subscribe((_token) => {
//        				localStorage.setItem('token', <string>_token);
//        			});
	  
  }
  
  //  вот как сделать срабатывание на кнопке. 
}
