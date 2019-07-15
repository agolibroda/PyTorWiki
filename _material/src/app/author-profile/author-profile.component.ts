import { Component, OnInit }                     from '@angular/core';
import { ActivatedRoute, Router }                 from '@angular/router';
import { Subscription }                         from 'rxjs';
import { first }                                 from 'rxjs/operators';
import { catchError, retry }                     from 'rxjs/operators';
//////////////////////
import { NgModule }                             from '@angular/core';
import { NgForm }                                 from '@angular/forms'; 
import { BrowserModule }                         from '@angular/platform-browser';
//import { AppComponent }                           from './app.component';


import { FormsModule, ReactiveFormsModule }     from '@angular/forms';
import { FormControl, FormGroup, FormBuilder, Validators }     from '@angular/forms';
//////////////////////

import { MAIN_COLOR, COLORS, ColorSelector }     from '../_config/colors';

import { Group }     from     '../_models/group';
import { Article }     from     '../_models/article';
import { Author }     from     '../_models/author';

import { AuthorDataService }         from '../_data_services/author-data.service';
import { ArticlesListDataService }     from '../_data_services/lists/article-list-data.service';
import { GroupListDataService }     from '../_data_services/lists/group-list-data.service';


@NgModule({
      imports:      [
//        CommonModule,
          BrowserModule,
        FormsModule,
        ReactiveFormsModule
      ],
        declarations: [ ],
      exports: [
//        CommonModule,
        FormsModule,
        ReactiveFormsModule
      ]
    })
    

@Component({
  selector: 'app-author-profile',
  templateUrl: './author-profile.component.html',
  styleUrls: ['./author-profile.component.css']
})

export class AuthorProfileComponent implements OnInit {

    
    isPwdEdit: boolean; //  флажок про закрытие/открытие зоны редактирования пароля
    authorProfile: Author; // описание Автора (заголовок)
    authorProfileSubscription: Subscription;
    articlesList: Article[]; // список статей
    groupsList: Group[]; // список групп, в которых Автор участник

    itemColor: ColorSelector;

//authorDataService: AuthorDataService;
    articlesListDataService: ArticlesListDataService;
    groupsListDataService: GroupListDataService;

    courseId: number;

    authorProfileForm: FormGroup;

    constructor(
            
            private formBuilder: FormBuilder,
             
            private authorDataService: AuthorDataService,
            private route: ActivatedRoute,
            private router: Router,
             
          ) {        
        
        this.itemColor = new ColorSelector();
        
        this.authorProfile = new Author();
        this.articlesList = [];
        this.groupsList = [];
    
        this.articlesListDataService = new ArticlesListDataService();
    
        this.groupsListDataService = new GroupListDataService();
    
//        this.authorProfileSubscription = this.authorDataService.authorProfile.subscribe(_author => {
//            this.authorProfile = _author;
//        });
//         console.log('AuthorProfileComponent:: constructor this.authorProfile = ' + JSON.stringify(this.authorProfile, null, 4));
    }
    
/**
 *
 * вот тут все несколько иначе - 
 * надо выдернуть ИД да и все данные из сессии - из редиски
 * и разместить данные в полях для редактирования.
 * 
 */    
    ngOnInit(): void {

      this.isPwdEdit = false;
        
      let authorProfileSou = localStorage.getItem('lsCurrentAuthor')
		//  в случае, если мы редактируем нового пользователя, тогда у него еще нет параметров в памяти, 
    //  и его не с фига загружать!
		if (!authorProfileSou) {
		  this.isPwdEdit = true;
		} else {
		  this.authorProfile = JSON.parse(authorProfileSou);
		  console.log('AuthorProfileComponent:: this.authorProfile = ' + JSON.stringify(this.authorProfile, null, 4));
		}
        
        let tokenSou = localStorage.getItem('token');
        console.log('AuthorProfileComponent:: tokenSou = ' + tokenSou);
        this.authorProfile.token = tokenSou; // JSON.parse(localStorage.getItem('token'));
        this.initForm();
        
        
    }
    
//    /**
//     *  Инициализация формы
//     *  
//     */
    initForm(){
		
      console.log('initForm ... this.isPwdEdit = ' + this.isPwdEdit);  

      this.authorProfileForm = this.formBuilder.group({ /*this.fb.group*/
                  dt_header_id:           [this.authorProfile.dt_header_id],
                  author_name:            [this.authorProfile.author_name, [
                                                        Validators.required,
                                                        Validators.pattern(/\W+/)
                                                       ]],
                  author_surname:         [this.authorProfile.author_surname, [
                                                        Validators.required,
                                                        Validators.pattern(/\W+/)
                                                       ]],
                  author_login:           [this.authorProfile.author_login, [
                                                        Validators.required,
                                                        Validators.pattern(/\W+/)
                                                       ]],
                  email:                  [this.authorProfile.author_email, [
                                                        Validators.email]], // 
                  author_phon:            [this.authorProfile.author_phon],
                  author_yourself_story:  [this.authorProfile.author_yourself_story],
                  token:                  [this.authorProfile.token],
                  oldPwd:                 '',
                  newPwd:                 '',
                  reEntryPwd:             ''

              });        
         }


    endEditPwd(setValue: boolean): void {
    // все нафиг закроем, и поля новых/сарых пролей почистим!!!
      this.isPwdEdit = setValue;
      if (!setValue) {
        this.authorProfile.oldPwd = '';
        this.authorProfile.newPwd =  '';
        this.authorProfile.reEntryPwd = '';
      }
    }
    
    /**
     * пока эта функция не имеет смысла!!!! все данные буду проверять после сабмита! 
     * 
     */
    isControlInvalid(controlName: string): boolean {
      console.log('isControlInvalid this.authorProfile = ');  
      console.log(this.authorProfile);  // -- вот ЭТО содержит данные!!!!!
//      console.log('isControlInvalid this.authorProfileForm = ');  
//      console.log(this.authorProfileForm);  -- вот ЭТО НЕ содержит новые данные!!!!! не понимаю почему, и бросаю маяться хернёй!
      
      console.log('isControlInvalid this.authorProfile.controls = ');  
      console.log(this.authorProfileForm.controls);  
//      const control = this.authorProfile.controls[controlName];
      const control = this.authorProfileForm.controls[controlName];
      console.log('isControlInvalid control = ');  
      console.log(control);  
      const result = control.invalid && control.touched;
      console.log('isControlInvalid ... controlName = ' +controlName+ '; '+ control.value + ';  result = ' + result);  
      return result;
    }    
    
    /**
     * проверить все данные, особенно пароль :-)  
     * 
     * 
     */
    onSubmit(): boolean {
          console.log('onSubmit ... this.authorProfile - есть данные. ');  // {first: 'Nancy', last: 'Drew'}
          console.log(this.authorProfile);  // {first: 'Nancy', last: 'Drew'}
          //  Стоит проверить, что хот что - то в данных поменялись, и, тогда и писать. 
          // Кстати, про изменения  - проверяем если поменялся пароль 
          // (есть три значения  - старый  - и 2 новых, причём, новые совпадают) 
          // вот тогда можно и проверить РСА ключи, вдруг их нету, тогда создать и всё записать.
          
          if (this.authorProfile.newPwd !== this.authorProfile.reEntryPwd ) {
            return false;
          }
          
          
          if (this.authorProfile.dt_header_id == 0) {
            // Это новый пользователь, this.authorProfile.oldPwd - тут не нужен
            this.authorProfile.oldPwd = '';
            
            // return 
            this.authorDataService.register(this.authorProfile)
//                      .pipe(catchError(this.authorDataService.handleError) )
//                      .subscribe((_authorProfile: Author) => {
                      .subscribe((_authorProfile) => {
                         return true;
                      });
            
          } else {
            // пользователь уже есть, и его данные надо обновить!
            // return 
            this.authorDataService.update(this.authorProfile)
//                      .pipe(catchError(this.authorDataService.handleError) )
//                      .subscribe((_authorProfile: Author) => {
                      .subscribe((_authorProfile) => {
                         return true;
                      });

          }
          
        }     

    /**
     *  "просмотр описания группы"
     * 
     *  Происходят следующие везчи:
     *   - выбрать надо описание группы (по номеру группы, естественно!)
     *   - выбрать весь (или первую страницу?) списка статей, которых есть в группе 
     *   - выбрать первую страницу Авторов, которые состоят в Группе.
     * 
     * 
     */
    getAuthor(authorId: number): void {
    // public authorId: number
            console.log('AuthorProfileComponent getGroup Start!!!  ' );
//            authorProfile: Author;
            
//            const authorId = 0 ; //+this.route.snapshot.paramMap.get('id');

            console.log('AuthorProfileComponent getAuthor authorId = ' + JSON.stringify(authorId, null, 4));

            if (authorId > 0) {
                this.authorDataService.getById(authorId)
                .pipe(catchError(this.authorDataService.handleError) )
                .subscribe((_authorProfile: Author) => {
                        console.log('AuthorViewComponent::: getAuthor _authorProfile = ' + JSON.stringify(_authorProfile, null, 4));
                        this.authorProfile = <Author>_authorProfile;
                        // Заберем список статей, Автора
                        this.articlesListDataService.getArticlesAutorList(authorId)
                        .then(_articlesList => {
                            // вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
                            // списка цветов, о которых знает система.
                            this.articlesList = _articlesList.map((article) => {
                                article.color = this.itemColor.get();//'primary';
                                return article;
                            });
//                            console.log('AuthorViewComponent::: getAuthor this.articlesList = ' + JSON.stringify(this.articlesList, null, 4));
                            // Заберем все группы автора
//                            return this.groupsListDataService.getAuthorGroupsList(authorId);
                        })
                        
                })
//                .catch(err => {
//                    console.log('getAuthor err = ' + JSON.stringify(err, null, 4));
//                }))
//                .then(_authorProfile => {
//                    // Заберем описание Автора
//                    this.authorProfile = <Author>_authorProfile
//                    console.log('getAuthor this.authorProfile = ' + JSON.stringify(this.authorProfile, null, 4));
//                    // Заберем список статей, Автора
//                    return this.articlesListDataService.getArticlesAutorList(authorId);
//                })
//                .then(_articlesList => {
//                    // вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
//                    // списка цветов, о которых знает система.
//                    this.articlesList = _articlesList.map((article) => {
//                        article.color = this.itemColor.get();//'primary';
//                        return article;
//                    });
//                    // Заберем все группы автора
//                    return this.groupsListDataService.getAuthorGroupsList(authorId);
//                })
//                .then(_groupsList => {
//                    // вот тут нужно перебрать все элементы списка статей, и в каждую всунуть цвет, который стоит взять из
//                    // списка цветов, о которых знает система.
//                    this.groupsList = _groupsList.map((group) => {
//                        group.color = this.itemColor.get();
//                        return group;
//                    });
                    
//                    this.groupsList = this.itemColor.setColors(_groupsList);
                    // положим авторов "куда надо"
//                });
                
            } else {
                // тут надо перейти к редактированию новой группы
//                this.authorProfile = new Author();
//                this.articlesList = [];
//                this.groupsList = [];
            }
            
        }

}
