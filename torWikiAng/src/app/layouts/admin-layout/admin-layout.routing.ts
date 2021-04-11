import { Routes } from '@angular/router';

import { AuthorViewComponent } 		from '../../author-view/author-view.component'; // просмотр профиля автора
import { AuthorProfileComponent } 	from '../../author-profile/author-profile.component'; // Редактирование Автором собственного профиля


import { AuthorsComponent } 		from '../../authors/authors.component'; // список авторов
import { GroupsComponent } 			from '../../groups/groups.component'; // список групп

import { ArticleComponent } 		from '../../article/article.component'; // просмотр/ редактирование статьи

import { GroupComponent } 			from '../../group/group.component'; // просмотр/редактирование группы

import { PageNotFoundComponent } 	from '../../page-not-found/page-not-found.component';
import { HomeComponent } 			from '../../home/home.component'; // главная страница

import { LoginComponent } 			from '../../login/login.component'; // Логин
import { LogoutComponent } 			from '../../logout/logout.component'; // logout

// import { TypographyComponent } from '../../typography/typography.component';


export const AdminLayoutRoutes: Routes = [
    // {
    //   path: '',
    //   children: [ {
    //     path: 'groups',
    //     component: GroupsComponent
    // }]}, {
    // path: '',
    // children: [ {
    //   path: 'userprofile',
    //   component: AuthorProfileComponent
    // }]
    // }, {
    //   path: '',
    //   children: [ {
    //     path: 'icons',
    //     component: IconsComponent
    //     }]
    // }, {
    //     path: '',
    //     children: [ {
    //         path: 'notifications',
    //         component: NotificationsComponent
    //     }]
    // }, {
    //     path: '',
    //     children: [ {
    //         path: 'maps',
    //         component: MapsComponent
    //     }]
    // }, {
    //     path: '',
    //     children: [ {
    //         path: 'typography',
    //         component: TypographyComponent
    //     }]
    // }, {
    //     path: '',
    //     children: [ {
    //         path: 'upgrade',
    //         component: UpgradeComponent
    //     }]
    // }
    { path: '',      			component: HomeComponent },
    { path: 'home',      		component: HomeComponent },
    { path: 'home/:id', 		component: HomeComponent },

    { path: 'authors', 			component: AuthorsComponent }, // список авторов
    { path: 'groups', 			component: GroupsComponent }, // список групп
    
    { path: 'author-profile', 	component: AuthorProfileComponent }, // редактировать СОБСТВЕННЫЙ профиль!
    { path: 'author/:id', 		component: AuthorViewComponent }, // просмотреть станицу автора
    
    { path: 'article', 			component: ArticleComponent }, // новая статья
    { path: 'article/:title',   component: ArticleComponent },  // чтение (редактирование) одной статьи

    { path: 'group',			component: GroupComponent},  // новая группа
    { path: 'group/:id',		component: GroupComponent},  // // просмотр (и редактирование??) одной групы
    
    { path: 'login', 			component: LoginComponent },
    { path: 'logout', 			component: LogoutComponent },
    
    { path: '**', 				component: PageNotFoundComponent },
  
  ];
