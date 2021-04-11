/**
 * Компонента для показа одной тумбочки одной группы..  
 * 
 * 
 * (c) A.Golibroda 2019
 * 
 */


import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-group-thumb',
  templateUrl: './group-thumb.component.html',
  styleUrls: ['./group-thumb.component.scss']
})
export class GroupThumbComponent implements OnInit {

	 @Input() groupThumbData: {};
	
  constructor() { }

  ngOnInit() {
  }

}
