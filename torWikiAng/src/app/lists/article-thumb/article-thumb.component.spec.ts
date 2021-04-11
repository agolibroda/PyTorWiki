import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleThumbComponent } from './article-thumb.component';

describe('ArticleThumbComponent', () => {
  let component: ArticleThumbComponent;
  let fixture: ComponentFixture<ArticleThumbComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ArticleThumbComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArticleThumbComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
