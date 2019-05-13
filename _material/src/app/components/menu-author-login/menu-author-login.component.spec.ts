import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MenuAuthorLoginComponent } from './menu-author-login.component';

describe('MenuAuthorLoginComponent', () => {
  let component: MenuAuthorLoginComponent;
  let fixture: ComponentFixture<MenuAuthorLoginComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MenuAuthorLoginComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MenuAuthorLoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
