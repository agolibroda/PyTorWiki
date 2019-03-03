import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AuthorThumbComponent } from './author-thumb.component';

describe('AuthorThumbComponent', () => {
  let component: AuthorThumbComponent;
  let fixture: ComponentFixture<AuthorThumbComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AuthorThumbComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AuthorThumbComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
