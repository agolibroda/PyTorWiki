import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GroupThumbComponent } from './group-thumb.component';

describe('GroupThumbComponent', () => {
  let component: GroupThumbComponent;
  let fixture: ComponentFixture<GroupThumbComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GroupThumbComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GroupThumbComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
