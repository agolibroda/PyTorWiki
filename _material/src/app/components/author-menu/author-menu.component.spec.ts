import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AuthorMenuComponent } from './author-menu.component';

describe('AuthorMenuComponent', () => {
  let component: AuthorMenuComponent;
  let fixture: ComponentFixture<AuthorMenuComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AuthorMenuComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AuthorMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
