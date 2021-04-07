import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-author-thumb',
  templateUrl: './author-thumb.component.html',
  styleUrls: ['./author-thumb.component.scss']
})
export class AuthorThumbComponent implements OnInit {

	 @Input() authorThumbData: {};

  constructor() { }

  ngOnInit() {
  }

}
