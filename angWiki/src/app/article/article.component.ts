/**
 * Компонента для показа одной статьи.  
 * 
 * 
 * (c) A.Golibroda 2019
 * 
 */

import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { Article } 	from 	'../_models/article';

import { ArticleDataService } 	from '../_data_services/article-data.service';


@Component({
  selector: 'app-article',
  templateUrl: './article.component.html',
  styleUrls: ['./article.component.css']
})

export class ArticleComponent implements OnInit {

	
	articleData: Article; // список статей-как-таковой

	constructor(
		    private articleDataService: ArticleDataService,
		    private readonly route: ActivatedRoute,
		  ) { }

  
	ngOnInit() {
		let articleTitle = this.route.snapshot.paramMap.get("title");
//		console.log('ngOnInit articleTitle = ' + JSON.stringify(articleTitle, null, 4));
		
		this.articleDataService.getByTitle(articleTitle)
		.subscribe((_articleData: Article) => {
			console.log('ArticleComponent _articleData = ' + JSON.stringify(_articleData, null, 4));
			// Заберем описание группы
			this.articleData = _articleData;
		})
	  
  }

}
