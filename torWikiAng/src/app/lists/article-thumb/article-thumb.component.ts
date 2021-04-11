/**
 * Компонента для показа одной тумбочки одной статьи..  
 * 
 * 
 * (c) A.Golibroda 2019
 * 
 */


import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-article-thumb',
  templateUrl: './article-thumb.component.html',
  styleUrls: ['./article-thumb.component.scss']
})
export class ArticleThumbComponent implements OnInit {

	
	 @Input() articleThumbData: {};
	
  constructor() { }

  ngOnInit() {
  }

}
