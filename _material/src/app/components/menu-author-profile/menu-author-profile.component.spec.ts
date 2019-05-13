import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MenuAuthorProfileComponent } from './menu-author-profile.component';

describe('MenuAuthorProfileComponent', () => {
  let component: MenuAuthorProfileComponent;
  let fixture: ComponentFixture<MenuAuthorProfileComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MenuAuthorProfileComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MenuAuthorProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
