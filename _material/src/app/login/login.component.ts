/**
 * 
 * import { LoginComponent }  from '../../login/login.component';
 * 
 */


import { Component, OnInit, Output } from '@angular/core';
import { NgForm} from '@angular/forms';
import { Router } from '@angular/router';

import { AuthorDataService } from '../_data_services/author-data.service';
//import { globals } from '../globals';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

	
	constructor(
			private authorLoginService: AuthorDataService,
			private router: Router
			) { 
	  
//	  this.successfulLogin$ = new EventEmitter<boolean>();
	}

  ngOnInit() {
  }

  
  public makeLogin (formData: NgForm) {

//	  console.log(formData.value.username);
//	  console.log(formData.value.password);
//	  console.log(formData.value.saveMe);
//	  console.log(formData);
	  
	  this.authorLoginService.login(
			  			formData.value.username, 
			  			formData.value.password, 
			  			formData.value.saveMe, // если флаг включен, то перца мы запомним на год :-) 
			  			localStorage.getItem('token')
			  			)
		 .subscribe((_afterLoginRezult) => {
       console.log('makeLogin _afterLoginRezult =  ' + JSON.stringify(_afterLoginRezult, null, 4));
			 // А, вот тут надо перепрыгнуть на какую - то другую страницу!!!!
			 // и, кстати, надо поменять ленку в шиблоне - с "логина" на мой профиль!!!!
			 // 	и, кстати, стоит перекинуть на главную. 
//	      console.log(globals);
			 
			 this.router.navigate(['/']);
		 });
	  
  }
  
  //  вот как сделать срабатывание на кнопке. 
}
