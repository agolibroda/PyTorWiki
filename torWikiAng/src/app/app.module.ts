import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
///////////////////////
import { ReactiveFormsModule } from '@angular/forms';
///////////////////////
// import { HttpModule } from '@angular/http';

import {HttpClientModule} from '@angular/common/http';

import { RouterModule } from '@angular/router';

import { BrowserModule, Title }  from '@angular/platform-browser';

import { AppRoutingModule } from './app.routing';
import { ComponentsModule } from './components/components.module';

import { AppComponent } from './app.component';

import { LoginComponent }     from './login/login.component';
import { LogoutComponent }    from './logout/logout.component'; // logout


import {
  AgmCoreModule
} from '@agm/core';
import { AdminLayoutComponent } from './layouts/admin-layout/admin-layout.component';


@NgModule({
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    
    FormsModule,
    ReactiveFormsModule,
    
    // HttpModule,
    HttpClientModule,

    ComponentsModule,
    RouterModule,
    AppRoutingModule,
//    AgmCoreModule.forRoot({
//      apiKey: 'YOUR_GOOGLE_MAPS_API_KEY'
//    })
  ],
  declarations: [
    AppComponent,
    AdminLayoutComponent,

  ],
  providers: [
	  
	  Title,
	  
  ],
  bootstrap: [AppComponent]
})
export class AppModule { 
	
}
