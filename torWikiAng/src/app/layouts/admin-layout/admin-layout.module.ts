// import { NgModule } from '@angular/core';
// import { RouterModule } from '@angular/router';
// import { CommonModule } from '@angular/common';
// import { FormsModule, ReactiveFormsModule } from '@angular/forms';

// import { AdminLayoutRoutes } from './admin-layout.routing';

import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import {MatButtonModule} from '@angular/material/button';
import {MatInputModule} from '@angular/material/input';
import {MatRippleModule} from '@angular/material/core';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatTooltipModule} from '@angular/material/tooltip';
import {MatSelectModule} from '@angular/material/select';

import { AdminLayoutRoutes } from './admin-layout.routing';
// import { DashboardComponent } from '../../dashboard/dashboard.component';
// import { UserProfileComponent } from '../../user-profile/user-profile.component';
// import { TableListComponent } from '../../table-list/table-list.component';
// import { TypographyComponent } from '../../typography/typography.component';
// import { IconsComponent } from '../../icons/icons.component';
// import { MapsComponent } from '../../maps/maps.component';
// import { NotificationsComponent } from '../../notifications/notifications.component';
// import { UpgradeComponent } from '../../upgrade/upgrade.component';


import { AuthorProfileComponent } from '../../author-profile/author-profile.component';
import { AuthorViewComponent } from '../../author-view/author-view.component';

import { GroupsComponent } from '../../groups/groups.component';
import { AuthorsComponent } from '../../authors/authors.component';
import { ArticleComponent } from '../../article/article.component';

import { GroupComponent } from '../../group/group.component';

import { PageNotFoundComponent } from '../../page-not-found/page-not-found.component';

import { HomeComponent } from '../../home/home.component';


import { LoginComponent }  from '../../login/login.component';
import { LogoutComponent } from '../../logout/logout.component'; // logout


import { AuthorThumbComponent } from '../../lists/author-thumb/author-thumb.component';
import { ArticleThumbComponent } from '../../lists/article-thumb/article-thumb.component';
import { GroupThumbComponent } from '../../lists/group-thumb/group-thumb.component';

import { ArticleListComponent } from '../../lists/article-list/article-list.component';


// import {
//   MatButtonModule,
//   MatInputModule,
//   MatRippleModule,
//   MatFormFieldModule,
//   MatTooltipModule,
//   MatSelectModule
// } from '@angular/material';

@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(AdminLayoutRoutes),
    FormsModule,
    MatButtonModule,
    MatRippleModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatTooltipModule,
  ],
  declarations: [
    GroupsComponent,
    AuthorsComponent,
    
    AuthorProfileComponent,
	AuthorViewComponent,
    
    ArticleComponent,
    GroupComponent,
    
    PageNotFoundComponent,
	HomeComponent,
	
	LoginComponent,
	LogoutComponent,
	
    AuthorThumbComponent,
    ArticleThumbComponent,
    GroupThumbComponent,
    
    ArticleListComponent,

  ],
  exports: [ RouterModule ]  
})

export class AdminLayoutModule {}
